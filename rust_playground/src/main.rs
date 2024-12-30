extern crate core;

use std::collections::{HashMap, HashSet};
use std::iter::FlatMap;
use std::ops::Range;
use itertools::Itertools;

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


    let this: [usize;4] = [0, 0, 1, 2];
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
}
