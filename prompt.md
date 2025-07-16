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
