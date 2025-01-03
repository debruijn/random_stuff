use itertools::Itertools;
use std::collections::HashMap;
use std::ops::Range;
use std::time::Instant;
use std::iter::FromIterator;

/// An iterator adaptor that iterates through all the unique multiset permutations of the iterator.
///  The supplied iterator is fully consumed, so it must be finite.
///
/// See [`.multiset_permutations()`](crate::Itertools::multiset_permutations) for
/// more information.
#[derive(Debug, Clone)]
pub struct MultisetPermutations<I> {
    buffer: Vec<I>,
    start: bool,
    index: usize,
}

pub fn multiset_permutations<I: Iterator>(iter: I) -> MultisetPermutations<I::Item>
where
    I: Iterator,
    I::Item: Ord,
{
    let mut buffer = Vec::from_iter(iter);
    buffer.sort_unstable_by(|a, b| b.cmp(a));
    let length = buffer.len();
    MultisetPermutations {
        buffer: buffer,
        start: true,
        index: length.saturating_sub(2),
    }
}

impl<I: Copy> Iterator for MultisetPermutations<I>
where
    I: Ord,
{
    type Item = Vec<I>;

    fn next(&mut self) -> Option<Self::Item> {
        // Start iteration with buffer itself
        if self.start {
            self.start = false;
            return Some(self.buffer.clone());
        }

        // Exhausted iteration
        let has_two_next = self.index + 2 < self.buffer.len();
        if !has_two_next
            && (self.buffer.len() <= self.index + 1
            || self.buffer[0] <= self.buffer[self.index + 1])
        {
            return None;
        }

        // Determine shift index
        let shift_index = if has_two_next && self.buffer[self.index + 2] <= self.buffer[self.index]
        {
            self.index + 2
        } else {
            self.index + 1
        };

        // Prefix shift
        let shift_elem = self.buffer[shift_index];
        let mut swap_index = shift_index;
        while swap_index > 0 {
            self.buffer[swap_index] = self.buffer[swap_index - 1];
            swap_index -= 1;
        }
        self.buffer[0] = shift_elem;

        // Update index
        if self.buffer[0] < self.buffer[1] {
            self.index = 0;
        } else {
            self.index += 1;
        }

        Some(self.buffer.clone())
    }
}

fn derangements_range(n: usize) -> Vec<Vec<usize>> {
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
                        if i == k {
                            temp.push(n - 1);
                        }
                        if *el == k {
                            *el = k + 1;
                        }
                        temp.push(*el)
                    }
                    if k == temp2.len() {
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

fn main() {
    let this: Range<usize> = 0..4;

    let mut perms = Vec::new();
    let mut derangs = Vec::new();
    for i in this.permutations(3) {
        if !i.iter().enumerate().any(|x| x.0 == *x.1) {
            derangs.push(i.clone());
        }
        perms.push(i);
    }

    println!("Permutations: {:?}", perms);
    println!("Derangements: {:?}", derangs);

    let this: [usize; 4] = [0, 0, 1, 2];
    let mut excl: HashMap<usize, Vec<usize>> = HashMap::new();
    excl.insert(0, vec![0, 1]);
    excl.insert(1, vec![2]);
    excl.insert(2, vec![3]);

    let mut perms = Vec::new();
    let mut derangs = Vec::new();
    let mut self_derangs = Vec::new();
    let mut excl_derangs = Vec::new();
    for i in this.into_iter().permutations(3) {
        if !i.iter().enumerate().any(|x| x.0 == *x.1) {
            derangs.push(i.clone());
        }
        if !i.iter().enumerate().any(|x| this[x.0] == *x.1) {
            self_derangs.push(i.clone());
        }
        if !i.iter().enumerate().any(|x| excl[&x.0].contains(x.1)) {
            excl_derangs.push(i.clone());
        }
        perms.push(i);
    }

    println!("Permutations: {:?}", perms);
    println!("Derangements: {:?}", derangs);
    println!("Self derangements: {:?}", self_derangs);
    println!("Excl derangements: {:?}", excl_derangs);

    let n = 10;

    {
        let this: [usize; 8] = [0, 0, 0, 1, 1, 2, 2, 3];
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in this.into_iter().permutations(8) {
            perms.push(i);
        }
        let after = Instant::now();
        println!("Permutations 8: {:?} in {:?}", perms.len(), after - before);
    }
    {
        let this: [usize; 8] = [0, 0, 0, 1, 1, 2, 2, 3];
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in Itertools::permutations(this.into_iter(), 8) {
            perms.push(i);
        }
        let after = Instant::now();
        println!("Permutations 8 alt: {:?} in {:?}", perms.len(), after - before);
    }
    {
        let this: [usize; 10] = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in this.into_iter().permutations(n) {
            perms.push(i);
        }
        let after = Instant::now();
        println!("Permutations 10: {:?} in {:?}", perms.len(), after - before);
    }
    {
        let this: [usize; 10] = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in this.into_iter().permutations(n).unique() {
            perms.push(i);
        }
        let after = Instant::now();
        println!(
            "Distinct permutations: {:?} in {:?}",
            perms.len(),
            after - before
        );
    }
    {
        let this: Vec<usize> = vec![0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in multiset_permutations(this.into_iter()) {
            perms.push(i);
        }
        let after = Instant::now();
        println!(
            "Distinct permutations alt: {:?} in {:?}",
            perms.len(),
            after - before
        );
    }
    {
        let this: [usize; 10] = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut derangs = Vec::new();
        for i in this.into_iter().permutations(n) {
            if !i.iter().enumerate().any(|x| x.0 == *x.1) {
                derangs.push(i);
            }
        }
        let after = Instant::now();
        println!("Derangements: {:?} in {:?}", derangs.len(), after - before);
    }
    {
        let this: [usize; 10] = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut derangs = Vec::new();
        for i in this.into_iter().permutations(n).unique() {
            if !i.iter().enumerate().any(|x| x.0 == *x.1) {
                derangs.push(i);
            }
        }
        let after = Instant::now();
        println!(
            "Distinct derangements: {:?} in {:?}",
            derangs.len(),
            after - before
        );
    }
    {
        let this: [usize; 10] = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3];
        let before = Instant::now();
        let mut derangs = Vec::new();
        for i in this.into_iter().permutations(n) {
            if !i.iter().enumerate().any(|x| x.0 == *x.1) {
                derangs.push(i);
            }
        }
        derangs = derangs.into_iter().unique().collect_vec();
        let after = Instant::now();
        println!(
            "Distinct derangements alt: {:?} in {:?}",
            derangs.len(),
            after - before
        );
    }
    {
        let before = Instant::now();
        let derangs = derangements_range(n);
        let after = Instant::now();
        println!(
            "Derangements range: {:?} in {:?}",
            derangs.len(),
            after - before
        );
    }
    {
        let this: Range<usize> = 0..n;
        let before = Instant::now();
        let mut derangs = Vec::new();
        for i in Itertools::permutations(this.into_iter(), n) {
            if !i.iter().enumerate().any(|x| x.0 == *x.1) {
                derangs.push(i);
            }
        }
        let after = Instant::now();
        println!(
            "Derangements range no range: {:?} in {:?}",
            derangs.len(),
            after - before
        );
    }

    for i in 2..n {
        let before = Instant::now();
        let derangs = derangements_range(i);
        let after = Instant::now();
        println!(
            "Derangements range {i}: {:?} in {:?}",
            derangs.len(),
            after - before
        );
    }

    let n = 11;
    {
        let this: Range<usize> = 0..n;
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in Itertools::permutations(this.into_iter(), n) {
            perms.push(i);
        }
        let after = Instant::now();
        println!(
            "Distinct permutations range alt: {:?} in {:?}",
            perms.len(),
            after - before
        );
    }


    {
        let this: Range<usize> = 0..n;
        let before = Instant::now();
        let mut perms = Vec::new();
        for i in multiset_permutations(this.into_iter()) {
            perms.push(i);
        }
        let after = Instant::now();
        println!(
            "Distinct permutations range alt: {:?} in {:?}",
            perms.len(),
            after - before
        );
    }

    {
        let this: Range<usize> = 0..n;
        let before = Instant::now();
        let perms = Vec::from_iter(multiset_permutations(this.into_iter()));
        let after = Instant::now();
        println!(
            "Distinct permutations range alt: {:?} in {:?}",
            perms.len(),
            after - before
        );
    }

}
