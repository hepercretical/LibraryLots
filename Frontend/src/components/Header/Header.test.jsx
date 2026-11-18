import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import Header from './Header.jsx';
test('provides the home link', () => {
  render(<Header />);
  expect(screen.getByRole('link')).toHaveAttribute('href', '/');
});
