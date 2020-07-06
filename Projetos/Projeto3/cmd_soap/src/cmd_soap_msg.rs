use std::collections::HashMap;
use byte_array::ByteArray;

use hex_literal::hex;
use sha2::{Sha256, Sha512, Digest};

use hyper::{Client; Call};


fn get_wsdl(env: i32){
    /*Devolve URL do WSDL do SCMD.

    Parameters
    ----------
    t : int
        WSDL a devolver: 0 para preprod, 1 para prod.

    Returns
    -------
    string
        URL do WSDL do SCMD.
    */
        
    wsdl = [
        0: "https://preprod.cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/CCMovelDigitalSignature.svc?wsdl";
        1: "https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/CCMovelDigitalSignature.svc?wsdl"
    ];
    // Get the function from switcher dictionary
    if env == 0 || env == 1 {
        return wsdl[env];
    } else {
        return "No valid WSDL";
    }
}

fn getclient(){
    /* Devolve o cliente de ligação ao servidor SOAP da CMD.

    Parameters
    ----------
    env: int
        WSDL a devolver: 0 para preprod, 1 para prod.
    timeout: int
        Valor máximo que espera para estabelever ligação com o servidor SOAP da CMD

    Returns
    -------
    Client
        Devolve o cliente de ligação ao servidor SOAP da CMD. Por defeito devolve o
        servidor de preprod.

    */

    let wsdl = get_wsdl(0);    
    let client = Client::new();
    
    // Await the response...
    return client.get(Uri::from_static(wsdl));
}


fn hashPrefix(hashtype: String, hash: String){
    /*Devolve a hash, à qual acrescenta o prefixo adequado ao hashtype utilizada.

    Parameters
    ----------
    hashtype : string ('SHA256')
        tipo de hash efetuada, do qual hash é o resultado.
    hash : byte
        hash digest

    Returns
    -------
    byte
        Devolve hash adicionada de prefixo adequado ao hashtype de hash utilizada.
    */

    let mut prefix = HashMap::new();
    
    let mut bytearray = ["0x30", "0x31", "0x30", "0x0d", "0x06", "0x09", "0x60", "0x86", "0x48", "0x01", "0x65", "0x03", "0x04", "0x02", "0x01", "0x05", "0x00", "0x04", "0x20"];
    prefix.insert(String::from("SHA256"), bytearray);

    return String::from(prefix.get(&hashtype)) + hash;
}


fn getcertificate(client: Client, args: args, application_id: String){
    /*Prepara e executa o comando SCMD GetCertificate.

    Parameters
    ----------
    client : Client (zeep)
        Client inicializado com o WSDL.
    args : argparse.Namespace
        argumentos a serem utilizados na mensagem SOAP.

    Returns
    -------
    str
        Devolve o certificado do cidadão e a hierarquia de certificação.
    */

    let mut request_data = HashMap::new();
    request_data.insert(String::from("applicationId"), application_id);
    request_data.insert(String::from("userId"), args[0]);

    return client.call(GetCertificate(request_data));
}

fn ccmovelsign(client: Client, args: args, application_id: String, docName: String){
    /*Prepara e executa o comando SCMD CCMovelSign.

    Parameters
    ----------
    client : Client (zeep)
        Client inicializado com o WSDL.
    args : argparse.Namespace
        argumentos a serem utilizados na mensagem SOAP.
    hashtype: Tipo de hash
        tipo de hash efetuada, do qual o digest args.hash é o resultado.

    Returns
    -------
    SignStatus(Code: xsd:string, Field: xsd:string, FieldValue: xsd:string, Message: xsd:string,
    ProcessId: xsd:string)
        Devolve uma estrutura SignStatus com a resposta do CCMovelSign.
    */
    

    let mut hasher = Sha256::new();  // create a Sha256 object
    hasher.update(b"Nobody inspects the spammish repetition");   // write input message    
    let hash = hasher.finalize();    // read hash digest and consume hasher

    let mut request = HashMap::new();
    request.insert(String::from("ApplicationId"), application_id);
    request.insert(String::from("UserId"), args[2]);
    request.insert(String::from("Pin"), args[3]);
    request.insert(String::from("Hash"), hash);
    request.insert(String::from("DocName"), docName);

    let mut request_data = HashMap::new();
    request_data.insert(String::from("request"), request);

    return client.call(CCMovelSign(request_data));
}


fn ccmovelmultiplesign(client: Client, args: args, application_id: String){
    /*Prepara e executa o comando SCMD CCMovelMultipleSign.

    Parameters
    ----------
    client : Client (zeep)
        Client inicializado com o WSDL.
    args : argparse.Namespace
        argumentos a serem utilizados na mensagem SOAP.

    Returns
    -------
    SignStatus
        Devolve uma estrutura SignStatus com a resposta do CCMovelMultipleSign.

    */
    
    // Documents
    let mut hasher = Sha256::new();  // create a Sha256 object
    hasher.update(b"Nobody inspects the spammish repetition");   // write input message    
    let hash = hasher.finalize();    // read hash digest and consume hasher

    let mut hasher2 = Sha256::new();  // create a Sha256 object
    hasher2.update(b"Always inspects the spammish repetition");   // write input message    
    let hash2 = hasher.finalize();    // read hash digest and consume hasher

    let hashstructure = [hash, hash2];

    let mut documents = HashMap::new();    
    documents.insert(String::from("HashStructure"), hashstructure);

    // Request
    let mut request = HashMap::new();
    request.insert(String::from("ApplicationId"), application_id);
    request.insert(String::from("UserId"), args[2]);
    request.insert(String::from("Pin"), args[3]);
    
    let mut request_data = HashMap::new();
    request_data.insert(String::from("request"), request);
    request_data.insert(String::from("documents"), documents);

    return client.call(CCMovelMultipleSign(request_data));
}


fn validate_otp(client: Client, args: args, application_id: String, otp_code: String, process_id: String){
    /*Prepara e executa o comando SCMD ValidateOtp.

    Parameters
    ----------
    client : Client (zeep)
        Client inicializado com o WSDL.
    args : argparse.Namespace
        argumentos a serem utilizados na mensagem SOAP.

    Returns
    -------
    SignResponse
        Devolve uma estrutura SignResponse com a resposta do CCMovelMultipleSign.

    */

    let mut request_data = HashMap::new();
    request_data.insert(String::from("ApplicationId"), application_id);
    request_data.insert(String::from("processID"), process_id);
    request_data.insert(String::from("code"), otp_code);

    return client.call(ValidateOtp(request_data));
}
