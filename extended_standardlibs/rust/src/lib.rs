
use pyo3::prelude::*;
use itertools::{repeat_n, Itertools};
use pyo3::{pyfunction};
use itertools;

type T = u8;

#[pyfunction]
fn derangements_range(n: T) -> Vec<Vec<T>> {
    match n {
        2 => vec![vec![1, 0]],
        1 => Vec::new(),
        0 => Vec::new(),
        _ => {
            let mut derangements = Vec::new();
            let lag1 = derangements_range(n - 1);
            for lag in lag1.iter() {
                for split in 0..lag.len() {
                    let mut temp = lag
                        .iter()
                        .enumerate()
                        .map(|x| if x.0 == split { n - 1 } else { *x.1 })
                        .collect_vec();
                    temp.push(lag[split]);
                    derangements.push(temp);
                }
            }

            let lag2 = derangements_range(n - 2);
            for lag in lag2.iter() {
                let mut temp = lag.clone();
                let mut temp2 = lag.clone();
                temp.push(n - 1);
                temp.push(n - 2);
                derangements.push(temp);

                for k in (0..n - 2).rev() {
                    let mut temp = Vec::new();
                    for (i, el) in temp2.iter_mut().enumerate() {
                        if i as u8 == k {
                            temp.push(n - 1);
                        }
                        if *el == k {
                            *el = k + 1;
                        }
                        temp.push(*el)
                    }
                    if k == temp2.len() as u8 {
                        temp.push(n - 1)
                    }
                    temp.push(k);

                    derangements.push(temp);
                }
            }
            derangements
        }
    }
}


#[pyfunction]
fn permutations<'a>(iterable: Vec<T>, k: T) -> Vec<Vec<T>> {
    iterable.into_iter().permutations(k as usize).collect_vec()
}

#[pyfunction]
fn distinct_permutations<'a>(iterable: Vec<T>, k: T) -> Vec<Vec<T>> {
    iterable.into_iter().permutations(k as usize).unique().collect_vec()
}

#[pyfunction]
fn derangements<'a>(iterable: Vec<T>, k: T) -> Vec<Vec<T>> {
    iterable.into_iter().permutations(k as usize).filter(|i| !i.iter().enumerate().any(|x| x.0 == *x.1 as usize)).collect_vec()
}

#[pyfunction]
fn combinations<'a>(iterable: Vec<T>, k: T) -> Vec<Vec<T>> {
    iterable.into_iter().combinations(k as usize).collect_vec()
}

#[pyfunction]
fn combinations_with_replacement<'a>(iterable: Vec<T>, k: T) -> Vec<Vec<T>> {
    iterable.into_iter().combinations_with_replacement(k as usize).collect_vec()
}

#[pyfunction]
fn pairwise<'a>(iterable: Vec<T>) -> Vec<(T, T)> {
    iterable.into_iter().tuple_windows().collect()
}

#[pyfunction]
fn repeat<'a>(n: T, k: T) -> Vec<T> {
    repeat_n(n, k as usize).collect_vec()
}


#[pyfunction]
fn powerset<'a>(iterable: Vec<T>) -> Vec<Vec<T>> {
    iterable.into_iter().powerset().collect_vec()
}

#[pymodule]
#[pyo3(name = "rust_itertools")]
pub fn rust_itertools(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(permutations, m)?)?;
    m.add_function(wrap_pyfunction!(distinct_permutations, m)?)?;
    m.add_function(wrap_pyfunction!(derangements, m)?)?;
    m.add_function(wrap_pyfunction!(combinations, m)?)?;
    m.add_function(wrap_pyfunction!(combinations_with_replacement, m)?)?;
    m.add_function(wrap_pyfunction!(pairwise, m)?)?;
    m.add_function(wrap_pyfunction!(repeat, m)?)?;
    m.add_function(wrap_pyfunction!(powerset, m)?)?;
    m.add_function(wrap_pyfunction!(derangements_range, m)?)?;
    Ok(())
}
//
// #[pymodule]
// #[pyo3(name = "rust_itertools_all")]
// pub fn rust_itertools_all(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_submodule(wrap_pymodule!(itertools)?)?;
//     Ok(())
// }
