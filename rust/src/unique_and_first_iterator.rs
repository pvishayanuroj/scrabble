use std::{collections::HashSet, hash::Hash};

/// Given a vector of N elements with M unique elements, this iterator returns a tuple of the
/// Mth element and a vector of the remaining N - 1 elements.
///
///  e.g. Given 'CATTO', this yields four iterations:
/// ('C', 'ATTO')
/// ('A', 'CTTO')
/// ('T', 'CATO')
/// ('O', 'CATT')
pub struct UniqueFirstAndRestIterator<'a, T: 'a>
where
    T: Hash + Eq,
{
    slice: &'a [T],
    curr_index: usize,
    unique_elements: Vec<&'a T>,
}

impl<'a, T> UniqueFirstAndRestIterator<'a, T>
where
    T: Hash + Eq,
{
    pub fn new(slice: &'a [T]) -> Self {
        if slice.len() == 0 {
            panic!("Input vector cannot be empty.");
        }

        let mut unique_elements = vec![];
        let mut seen = HashSet::new();
        for element in slice {
            if !seen.contains(element) {
                unique_elements.push(element);
                seen.insert(element);
            }
        }

        UniqueFirstAndRestIterator {
            slice,
            curr_index: 0,
            unique_elements,
        }
    }
}

impl<'a, T> Iterator for UniqueFirstAndRestIterator<'a, T>
where
    T: Hash + Eq,
{
    type Item = (&'a T, Vec<&'a T>);

    fn next(&mut self) -> Option<Self::Item> {
        if self.curr_index < self.unique_elements.len() {
            let curr_element = self.unique_elements[self.curr_index];
            let mut remainder = vec![];
            let mut first_occurence_found = false;
            // Remove the first occurrence of the element being returned.
            for element in self.slice {
                if *curr_element == *element && !first_occurence_found {
                    first_occurence_found = true;
                } else {
                    remainder.push(element);
                }
            }
            self.curr_index += 1;
            Some((curr_element, remainder))
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unique_first_and_rest_iterator() {
        let array = vec!['C', 'A', 'T', 'T', 'O'];
        let iterator = UniqueFirstAndRestIterator::new(&array);

        let result: Vec<(&char, Vec<&char>)> = iterator.collect();

        let expected = vec![
            (&'C', vec![&'A', &'T', &'T', &'O']),
            (&'A', vec![&'C', &'T', &'T', &'O']),
            (&'T', vec![&'C', &'A', &'T', &'O']),
            (&'O', vec![&'C', &'A', &'T', &'T']),
        ];
        assert_eq!(result, expected);
    }
}
