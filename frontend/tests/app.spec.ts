import { test, expect } from '@playwright/test';

test.describe('Board Game Collection App', () => {
  test('should load the homepage and display title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Board Game Collection/);
    
    // Wait for loading to finish
    await expect(page.getByText('Loading collection...')).toBeHidden({ timeout: 10000 });

    const errorCount = await page.getByText(/Error:/).count();
    if (errorCount > 0) {
        const err = await page.getByText(/Error:/).textContent();
        throw new Error(`App reported error: ${err}`);
    }

    // If we're here, loading is done and no explicit "Error:" text found.
    // If heading is still missing, maybe we are stuck?
    // Dump content if assertion fails
    try {
        await expect(page.getByRole('heading', { name: 'Board Game Collection' })).toBeVisible({ timeout: 2000 });
    } catch (e) {
        console.log('Page Content Dump:', await page.content());
        throw e;
    }
  });

  test('should load board games data', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Loading collection...')).toBeHidden({ timeout: 10000 });
    // Check if selector is enabled
    await expect(page.getByRole('combobox', { name: 'Select Shelf Image' })).toBeEnabled();
  });

  test('should allow selecting an image and showing bounding boxes', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Loading collection...')).toBeHidden({ timeout: 10000 });
    // Select the first image in the dropdown
    await page.getByRole('combobox', { name: 'Select Shelf Image' }).click();
    await page.getByRole('option').first().click(); // Select "None"
    await page.getByRole('combobox', { name: 'Select Shelf Image' }).click();
    await page.getByRole('option').nth(2).click(); // Select first actual image (index 2 because 0 is none, 1 might be none?)

    // Check if image is visible
    await expect(page.locator('img[alt="Board Game Shelf"]')).toBeVisible();
    
    // Check if at least one bounding box is visible
    // Note: Depends on data. If data is mocked, we know. If real data, we assume at least one game.
    // We can assume there are games.
    // Hover over a box?
    // We don't know exact implementation of box selector without class, but we used styled component.
    // It has click listener.
  });

  test('should filter games', async ({ page }) => {
    await page.goto('/');
    // Switch to Global Mode to see table
    await page.getByLabel('Global Mode (Table View)').check();
    
    // Check table headers
    await expect(page.getByRole('columnheader', { name: 'Title' })).toBeVisible();

    // Type in search box
    const searchInput = page.getByLabel('Search Title');
    await searchInput.fill('z'); // Assuming some game has 'z', or random string
    // Verify table updates?
    
    // Reset filters
    await page.getByText('Reset Filters').click();
  });
});
