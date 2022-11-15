import boto3
import dateutil.parser

s3_client = boto3.client("s3")
db_client = boto3.client('dynamodb')

TABLE_NAME = "NOME_DA_SUA_TABELA"
CSV_SEPARATOR = b";"

def read_csv_lines(event):
  bucket_name = 'NOME_DO_SEU_BUCKET'
  object_key = 'NOME_DO_ARQUIVO.EXTENSAO'

  return s3_client.get_object(Bucket=bucket_name, Key=object_key)["Body"].read().split(b'\n')

def process_line(line):
  data = line.split(CSV_SEPARATOR)
  
  # process data
  originador = data[0].decode()
  doc_originador = data[1].decode().translate({ord(i): None for i in '.-/'})
  cedente = data[2].decode()
  doc_cedente = data[3].decode().translate({ord(i): None for i in '.-/'})
  ccb = data[4].decode()
  id_externo = data[5].decode()
  id_cessao = str(hash(int(id_externo)))
  cliente = data[6].decode()
  cpf_cnpj = data[7].decode()
  endereco = data[8].decode()
  cep = data[9].decode()
  cidade = data[10].decode()
  uf = data[11].decode()
  valor_do_emprestimo = data[12].decode()
  valor_parcela = data[14].decode()
  total_parcelas = data[19].decode()
  parcela = data[20].decode()
  data_de_emissao_str = data[23].decode()
  data_de_emissao = dateutil.parser.parse(data_de_emissao_str).strftime("%Y-%m-%d")
  data_de_vencimento_str = data[24].decode()
  data_de_vencimento = dateutil.parser.parse(data_de_vencimento_str).strftime("%Y-%m-%d")
  preco_de_aquisicao = data[26].decode()

  # save
  data = db_client.put_item(
    TableName=TABLE_NAME,
    Item={
      "ID_CESSAO": {
        "S": id_cessao
      },
      "CCB": {
        "S": ccb
      },
      "CEDENTE": {
        "S": cedente
      },
      "CEP": {
        "S": cep
      },
      "CIDADE": {
        "S": cidade
      },
      "CLIENTE": {
        "S": cliente
      },
      "CPF_CNPJ": {
        "S": cpf_cnpj
      },
      "DATA_DE_EMISSAO": {
        "S": data_de_emissao
      },
      "DATA_DE_VENCIMENTO": {
        "S": data_de_vencimento
      },
      "DOC_CEDENTE": {
        "S": doc_originador
      },
      "DOC_ORIGINADOR": {
        "S": doc_originador
      },
      "ENDERECO": {
        "S": endereco
      },
      "ID_EXTERNO": {
        "S": id_externo
      },
      "ORIGINADOR": {
        "S": originador
      },
      "PARCELA": {
        "S": parcela
      },
      "PRECO_DE_AQUISICAO": {
        "S": preco_de_aquisicao
      },
      "TOTAL_PARCELAS": {
        "S": total_parcelas
      },
      "UF": {
        "S": uf
      },
      "VALOR_DO_EMPRESTIMO": {
        "S": valor_do_emprestimo
      },
      "VALOR_PARCELA": {
        "S": valor_parcela
      }
    }
  )

def lambda_handler(event, context):
  lines = read_csv_lines(event)

  for line in lines:
    process_line(line)

  response = {
      'statusCode': 200,
      'body': 'success',
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
  }
  
  return response