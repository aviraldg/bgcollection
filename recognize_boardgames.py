import argparse
import json
import os
import time
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from PIL import Image
import dspy
from dspy.teleprompt import BootstrapFewShot
from bgg_api import BggApi

class BoardGame(BaseModel):
    """
    Pydantic model for a single board game.
    """
    box_2d: Tuple[float, float, float, float] = Field(..., description="The bounding box for the board game or expansion in [y_min, x_min, y_max, x_max] format.")
    title: Optional[str] = Field(..., description="The name of the board game or expansion. Set to null if the name is unclear.")
    description: str = Field(..., description="A description of what the box looks like.")
    location: str = Field(..., description="A description of where the game is located.")
    filename: str = Field(..., description="The filename the board game or expansion was found in.")

class BoardGameList(BaseModel):
    """
    Pydantic model for a list of board games.
    """
    games: List[BoardGame]

class RecognizeGamesSignature(dspy.Signature):
    """
    You are an expert at board games and identifying them.

    Context: The .jpg files in this directory are pictures of shelves with board games on them. The shelves also include expansions
    for board games.

    Task: Identify the games, and write them to a file called boardgames.json with the following schema:

    Schema:
    * box_2d - The bounding box for the board game or expansion in [y_min, x_min, y_max, x_max] format.
    * title - The name of the board game or expansion. e.g. Scrabble. IMPORTANT: This should be set to null if the name of
      the game is unclear from the image.
    * description - A description of what the box looks like e.g. "Green medium sized box with the letters SCRABBLE in
      white". Be as descriptive as possible.
    * location - A description of where the game is located e.g. Bottom shelf, middle stack, nest to Scrabble
    * filename - The filename the board game or expansion was found in.

    NOTE: It may not be possible to identify the names of all games as some of the titles may be obscured in the pictures.
    In this case it is still important to catalogue them so a human can identify them manually. Follow the instructions
    above to identify such cases by setting the title to null.
    """
    image_paths: List[str] = dspy.InputField(desc="A list of paths to the images to process.")
    games: BoardGameList = dspy.OutputField(desc="A list of board games found in the images.")

class GameRecognitionModule(dspy.Module):
    """
    A dspy module for recognizing board games in images.
    """
    def __init__(self):
        super().__init__()
        self.recognize_games = dspy.ChainOfThought(RecognizeGamesSignature)
        self.bgg_api = BggApi()

    def forward(self, image_paths: List[str]) -> BoardGameList:
        """
        Forward pass of the module.

        Args:
            image_paths: A list of paths to the images to process.

        Returns:
            A BoardGameList object containing the recognized games.
        """
        bgg_tool = dspy.Tool(
            func=self.bgg_api.get_bgg_game_details,
            name="BGG Search",
            desc="Searches for a board game on BoardGameGeek and returns its details.",
            args={"game_title": {"type": "string"}},
            arg_desc={"game_title": "The title of the game to search for."}
        )
        # The Gemini model can handle image paths directly.
        images = [Image.open(path) for path in image_paths]
        result = self.recognize_games(image_paths=images, tools=[bgg_tool])
        return result.games

def validation_metric(gold, pred, trace=None):
    """A simple validation metric based on matching game titles."""
    gold_titles = sorted([game.title for game in gold.games])
    try:
        pred_titles = sorted([game.title for game in pred.games])
    except Exception:
        return 0.0
    return 1.0 if gold_titles == pred_titles else 0.0

def main():
    """
    Main function to recognize board games from images.
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Recognize board games in images.")
    parser.add_argument("image_dir", help="Directory containing the image files.")
    parser.add_argument("--optimize", action="store_true", help="Optimize the prompt before running.")
    args = parser.parse_args()

    # Set up the Gemini LLM
    gemini = dspy.LM(model="gemini/gemini-1.5-pro", api_key="AIzaSyBbCddhy4k62LAM56RdDq1ahYPdCncZGiY")
    dspy.settings.configure(lm=gemini)

    # Initialize the dspy module
    recognizer = GameRecognitionModule()

    if args.optimize:
        print("Optimizing the prompt...")
        # Load training data
        with open("training_data.json", "r") as f:
            training_data = json.load(f)

        # Create dspy.Example objects
        trainset = []
        for example in training_data:
            expected_games_list = BoardGameList(games=[BoardGame(**g) for g in example["expected_games"]["games"]])
            trainset.append(dspy.Example(image_paths=[example["image_path"]], games=expected_games_list).with_inputs("image_paths"))

        # Set up the optimizer
        config = dict(max_bootstrapped_demos=2, max_labeled_demos=2)
        teleprompter = BootstrapFewShot(metric=validation_metric, **config)
        recognizer = teleprompter.compile(student=GameRecognitionModule(), trainset=trainset)
        print("Optimization complete.")

    all_games = []
    image_files = [f for f in os.listdir(args.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        image_path = os.path.join(args.image_dir, image_file)
        try:
            print(f"Processing image: {image_path}")
            recognized_games = recognizer.forward(image_paths=[image_path])
            all_games.extend(recognized_games.games)
            # Add a delay to avoid hitting the rate limit
            time.sleep(60)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    print(json.dumps({"games": [game.dict() for game in all_games]}, indent=2))

if __name__ == "__main__":
    main()
