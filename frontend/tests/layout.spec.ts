import { test, expect } from '@playwright/test';

test.describe('Layout Regression', () => {
  test('should position info tags correctly on initial load', async ({ page }) => {
    await page.goto('/');
    
    // Select image containing Doomlings (first image in list usually, or we select explicit)
    // Doomlings is in PXL_20250715_164054770.MP.jpg
    // We need to select that image.
    await page.getByRole('combobox', { name: 'Select Shelf Image' }).click();
    await page.getByRole('option', { name: 'Right Shelf', exact: true }).click();

    // Wait for image to load but NOT for everything to settle? 
    // The bug is that they show up at 0,0 THEN jump.
    // So we check immediately when they appear.
    
    // Find the box for Doomlings
    // The tooltips trigger doesn't have text unless alwaysShowInfo is true.
    // alwaysShowInfo IS true by default.
    // So we should find text "Doomlings".
    
    const doomlingsLabel = page.getByText('Doomlings', { exact: true });
    await expect(doomlingsLabel).toBeVisible();

    // Get the bounding box of the element
    const box = await doomlingsLabel.boundingBox();
    if (!box) throw new Error('Doomlings box not found');

    // Check if it is NOT at top left (0,0 relative to something).
    // Actually we want check its absolute position on page.
    // If bug: it's at 0,0 relative to image container.
    // Image container is centered/margined.
    // But if scale is 0, all boxes are bunched at 0,0 of the image container.
    
    // Doomlings x1 is 255.
    // Even if image is small, it should be offset from the container's left edge.
    // Let's check if 'left' style is not '0px'.
    // We need to get the parent of the text, which is InfoTag, parent is StyledBox.
    // StyledBox has the style left/top.
    
    // doomlingsLabel is 'Doomlings' text node or element containing it.
    
    // doomlingsLabel is 'Doomlings' text node or element containing it.
    // Structure: StyledBox > InfoTag > [text]
    // If strict match text 'Doomlings' is inside <strong>...
    // Structure: StyledBox > InfoTag > strong > [text]
    // So we might need 3 levels up?
    // Let's use xpath ancestor to be safe.
    // StyledBox has explicit style attribute.
    
    // Find closest ancestor with style attribute containing 'left'
    const styledBox = doomlingsLabel.locator('xpath=ancestor::div[contains(@style, "left")]').first();
    
    await expect(styledBox).toBeVisible();
    await expect(styledBox).toHaveAttribute('style', /left/);
    
    const style = await styledBox.getAttribute('style');
    console.log('Doomlings Style:', style);
    
    // If bug, left might be "0px" or very close to it if scale is 0.
    // If data says 255, and scale is 0, left is 0.
    
    // Assert left is not 0px.
    // Note: style string might be "left: 0px; top: 0px; ..."
    expect(style).not.toContain('left: 0px');
    expect(style).not.toContain('top: 0px');
  });
});
