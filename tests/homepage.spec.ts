import { test, expect } from '@playwright/test';

test.describe('The Internet - Homepage Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the homepage before each test
    await page.goto('https://the-internet.herokuapp.com');
  });

  test('should load homepage successfully', async ({ page }) => {
    // Verify page title
    await expect(page).toHaveTitle(/The Internet/);
    
    // Verify main heading is visible
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();
    await expect(heading).toHaveText('Welcome to the-internet');
  });

  test('should display available examples', async ({ page }) => {
    // Verify the subtitle
    const subtitle = page.locator('h2');
    await expect(subtitle).toBeVisible();
    await expect(subtitle).toContainText('Available Examples');
    
    // Verify the list of examples exists
    const examplesList = page.locator('ul');
    await expect(examplesList).toBeVisible();
  });

  test('should have working navigation links', async ({ page }) => {
    // Get all links in the examples list
    const links = page.locator('ul li a');
    const count = await links.count();
    
    // Verify there are multiple example links
    expect(count).toBeGreaterThan(0);
    
    // Check first link is clickable
    const firstLink = links.first();
    await expect(firstLink).toBeVisible();
    await expect(firstLink).toHaveAttribute('href');
  });

  test('should navigate to A/B Testing page', async ({ page }) => {
    // Click on A/B Testing link
    await page.click('text=A/B Testing');
    
    // Verify navigation to A/B Testing page
    await expect(page).toHaveURL(/\/abtest/);
    
    // Verify page content
    const heading = page.locator('h3');
    await expect(heading).toBeVisible();
  });

  test('should navigate to Add/Remove Elements page', async ({ page }) => {
    // Click on Add/Remove Elements link
    await page.click('text=Add/Remove Elements');
    
    // Verify navigation
    await expect(page).toHaveURL(/\/add_remove_elements/);
    
    // Verify page heading
    const heading = page.locator('h3');
    await expect(heading).toHaveText('Add/Remove Elements');
  });

  test('should navigate to Form Authentication page', async ({ page }) => {
    // Click on Form Authentication link
    await page.click('text=Form Authentication');
    
    // Verify navigation
    await expect(page).toHaveURL(/\/login/);
    
    // Verify login form is present
    const loginForm = page.locator('#login');
    await expect(loginForm).toBeVisible();
  });

  test('should have footer with Elemental Selenium link', async ({ page }) => {
    // Verify footer exists
    const footer = page.locator('#page-footer');
    await expect(footer).toBeVisible();
    
    // Verify Elemental Selenium link
    const footerLink = footer.locator('a');
    await expect(footerLink).toBeVisible();
    await expect(footerLink).toHaveAttribute('href', 'http://elementalselenium.com/');
  });
});
