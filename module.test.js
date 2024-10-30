// module.test.js
import mut from './module.js'; 


test('Testing div -- simple division', () => {
  const expected = 5;
  const got = mut.div(10, 2);
  expect(got).toBe(expected);
});

test('Testing div -- division by 1', () => {
  const expected = 15;
  const got = mut.div(15, 1);
  expect(got).toBe(expected);
});

test('Testing div -- division by 0', () => {
  const got = mut.div(10, 0);
  expect(got).toBe(Infinity); // JavaScript returns Infinity for division by 0
});

test('Testing div -- negative numbers', () => {
  const expected = -5;
  const got = mut.div(-10, 2);
  expect(got).toBe(expected);
});

test('Testing div -- decimal division', () => {
  const expected = 2.5;
  const got = mut.div(5, 2);
  expect(got).toBeCloseTo(expected);
});

// Test cases for containsNumbers()
test('Testing containsNumbers -- text with numbers', () => {
  const text = "hello123";
  const got = mut.containsNumbers(text);
  expect(got).toBe(true);
});

test('Testing containsNumbers -- text without numbers', () => {
  const text = "hello";
  const got = mut.containsNumbers(text);
  expect(got).toBe(false);
});

test('Testing containsNumbers -- text with numbers only', () => {
  const text = "12345";
  const got = mut.containsNumbers(text);
  expect(got).toBe(true);
});

test('Testing containsNumbers -- empty string', () => {
  const text = "";
  const got = mut.containsNumbers(text);
  expect(got).toBe(false);
});

test('Testing containsNumbers -- special characters', () => {
  const text = "hello!@#";
  const got = mut.containsNumbers(text);
  expect(got).toBe(false);
});


test('Testing sum -- success', () => {
    const expected = 30;
    const got = mut.sum(12, 18);
    expect(got).toBe(expected);
  });