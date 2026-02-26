# Module 08 / Project 04 — Property-Based Testing

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- The Hypothesis library for property-based testing
- `@given` decorator to generate random test inputs
- Strategies: `st.text`, `st.integers`, `st.lists`, `st.dictionaries`
- Testing properties (invariants) instead of specific examples

## Why this project exists

Normal tests check specific examples: "sort [3,1,2] and expect [1,2,3]". Property-based tests check general truths: "sorting any list should produce a list where every element is less than or equal to the next". Hypothesis generates hundreds of random inputs — including edge cases you would never think of — and checks that your properties hold for all of them. This is how you find the bugs that hide in unusual inputs like empty strings, negative numbers, and Unicode characters.

## Run

```bash
cd projects/modules/08-testing-advanced/04-property-based
pytest tests/test_properties.py -v
```

## Expected output

```text
tests/test_properties.py::test_sort_is_idempotent PASSED
tests/test_properties.py::test_sort_preserves_length PASSED
tests/test_properties.py::test_sort_elements_are_ordered PASSED
tests/test_properties.py::test_reverse_twice_is_original PASSED
tests/test_properties.py::test_reverse_preserves_length PASSED
tests/test_properties.py::test_encode_decode_roundtrip PASSED
tests/test_properties.py::test_merge_dicts_contains_all_keys PASSED
tests/test_properties.py::test_merge_dicts_second_wins_on_conflict PASSED
```

Hypothesis runs each test with many different random inputs. If any input causes a failure, Hypothesis shrinks it to the simplest failing example and shows it to you.

## Alter it

1. Add a property test for `sort_list` that checks: every element in the sorted output was present in the original input (no elements added or removed).
2. Write a property test for `reverse_string` using only alphabetic text (`st.text(alphabet=st.characters(whitelist_categories=("L",)))`) and verify that reversing preserves the set of characters.
3. Add a property test for `merge_dicts` with `st.dictionaries(st.text(min_size=1), st.integers())` and verify the result length is at most the sum of the input lengths.

## Break it

1. Introduce a subtle bug in `sort_list`: make it drop duplicate elements (use `list(set(lst))` before sorting). Run the property tests and see which one catches it.
2. Break `encode_decode_json` by changing the encode step to strip whitespace. Hypothesis will find an input where the roundtrip fails.
3. Remove the `@given` decorator from one test and run it. It becomes a normal test with no inputs — it will either error or do nothing.

## Fix it

1. Revert the bugs you introduced. Run the tests to confirm they all pass.
2. If Hypothesis found a failing case you did not expect, add it as an explicit `@example` decorator so it is always tested.
3. Think about whether your property is actually correct, or if you need to weaken it.

## Explain it

1. What is the difference between example-based testing and property-based testing?
2. What does Hypothesis do when it finds a failing input? (Hint: "shrinking")
3. Why is "sort twice equals sort once" (idempotency) a useful property to test?
4. What kinds of bugs does property-based testing find that example-based testing misses?

## Mastery check

You can move on when you can:

- Write a `@given` decorator with appropriate strategies from memory.
- Identify at least two properties for any function you are given.
- Explain what shrinking means and why it helps debugging.
- Describe when property-based testing is more valuable than example-based testing.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Decorators Explained](../../../../concepts/decorators-explained.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

[Project 05 — Integration Testing](../05-integration-testing/)
