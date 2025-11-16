import { test, expect } from '@playwright/test';

const selectors = {
  username: 'input[placeholder="admin@nebula"]',
  password: 'input[type="password"]'
};

test('user can authenticate and view dashboard metrics', async ({ page }) => {
  await page.goto('/login');
  await page.fill(selectors.username, 'demo-admin');
  await page.fill(selectors.password, 'demo-password');
  await page.getByRole('button', { name: /sign in/i }).click();

  await expect(page.getByText('Live deployment overview')).toBeVisible();
  await expect(page.getByText('Successful deployments')).toBeVisible();
  await expect(page.getByText('Log stream')).toBeVisible();
});
