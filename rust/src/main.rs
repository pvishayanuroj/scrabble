use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    match read_lines("testcases/test3_state.txt") {
        Ok(lines) => {
            for line in lines.flatten() {
                println!("{}", line);
            }
        }
        Err(err) => eprintln!("Error occurred trying to read file: {err}"),
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
