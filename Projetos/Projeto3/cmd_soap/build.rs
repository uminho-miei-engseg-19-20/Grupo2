use std::env;   
use savon;

fn main() {
    println!("cargo:rustc-env=APPLICATION_ID=b826359c-06f8-425e-8ec3-50a97a418916");
    env::set_var("OUT_DIR", "/home/mata/MEI/2SEM/ES/Projeto3/cmd_soap/output");

    // Load Savon
    // let mut out_dir = env::var("OUT_DIR").unwrap();
    // let s = savon::gen::gen_write("./Weather.wsdl", &out_dir).unwrap();

   
}
