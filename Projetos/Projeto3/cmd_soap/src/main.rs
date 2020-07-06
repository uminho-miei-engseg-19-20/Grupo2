use std::env;
use std::fs;
use std::collections::HashMap;
use ::std::*;
use byte_array::ByteArray;

use hex_literal::hex;
use sha2::{Sha256, Sha512, Digest};

use hyper::{Client; Call};
use base64;

mod cmd_soap_msg;


// ARGS:
// [0] projeto
// [1] ficheiro
// [2] userid
// [3] pin

// Função main do programa
fn main(){
    let app_id = env::var("APPLICATION_ID").unwrap();
    
    // Verificar se application_id está definido
    if app_id.trim().is_empty(){
        println!("Configure o APPLICATION_ID");            
    }
    // Obter elementos da linha de comandos
    let args: Vec<String> = env::args().collect();
    // Verificar que foram passados elementos
    if args.len() > 1 {
        println!("app id : {} ", app_id);
        println!("{:?}", args);
        
        let user = &args[0];
        let pin = &args[1];
        let client = cmd_soap_msg::getclient();
        testall(client, args, app_id);
            
    } else{
        println!("Use -h for usage:\n {} -h for all operations\n {} <oper1> -h for usage of operation <oper1>", args[0], args[0]);
    }
}

fn testall(client: Client, args: args, application_id: String){
    // Prepara e executa todos os comandos SCMD em sequência.
    println!("Test All inicializado +++\n");
    print("0% ... Leitura de argumentos da linha de comando - file: " + args.file + " user: "
          + args.user + " pin: " + args.pin);
    println!("10% ... A contactar servidor SOAP CMD para operação GetCertificate");

    cmd_certs = cmd_soap_msg::getcertificate(client, args, application_id);
    println!("20% ... Certificado emitido para...");
    print("30% ... Leitura do ficheiro " + args[1])

    // ler ficheiro
    let file_content = fs::read_to_string(args[1])
        .expect("Ficheiro não encontrado.");

    println!("40% ... Geração de hash do ficheiro " + args[1]);
    let mut hasher = Sha256::new();  // create a Sha256 object
    hasher.update(file_content);   // write input message    
    let hash = hasher.finalize();    // read hash digest and consume hasher


    println!("60% ... A contactar servidor SOAP CMD para operação CCMovelSign");
    let docName = file_content;
    let res = cmd_soap_msg::ccmovelsign(client, args, application_id, docName);
    if res['Code'] != "200"{
        println!("Erro " + res['Code'] + ". Valide o PIN introduzido.");
        exit();
    }

    let processID = res['ProcessId']
    println!("70% ... ProcessID devolvido pela operação CCMovelSign: " + res['ProcessId'])
    println!("80% ... A iniciar operação ValidateOtp");
    println!("Introduza o OTP recebido no seu dispositivo:");
    let mut otp_code = String::new();
    io::stdin::().read_line(&mut otp_code).expect("Erro ao ler código.");
    
    println!("90% ... A contactar servidor SOAP CMD para operação ValidateOtp");
    res = cmd_soap_msg::validate_otp(client, args, application_id, otp_code, processID);

    if res['Status']['Code'] != '200'{
        print("Erro " + res['Status']['Code'] + ". " + res['Status']['Message']);
        exit();
    }


    println!("100% ... Assinatura (em base 64) devolvida pela operação ValidateOtp: " + base64::encode(&res['signature']);
    println!("110% ... A validar assinatura ...");


    // TODO:
    // digest = SHA256.new()
    // digest.update(file_content)
    // public_key = RSA.import_key(certs[0].as_bytes())
    // verifier = PKCS1_v1_5.new(public_key)
    // verified = verifier.verify(digest, res['Signature'])
    // assert verified, 'Falha na verificação da assinatura'
    // print('Assinatura verificada com sucesso, baseada na assinatura recebida, na hash gerada e ' +
    //       'na chave pública do certificado de ' + certs_chain['user'].get_subject().CN)
    // return '\n+++ Test All finalizado +++\n'


}
