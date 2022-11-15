
# Lambda Handler

Função a ser executada em lambdas AWS. Esta aplicação recebe dois parâmetros (bucket_name e object_key), referente a um arquivo CSV
em um bucket do s3, via requisição HTTP. A função ler o arquivo no bucket, trata as
informações e salva em uma tabela do DynamoDB.


## Configurações

### Passo 1

Faça login na sua conta da AWS [clique aqui](https://console.aws.amazon.com/console/home?nc2=h_ct&src=header-signin).
Caso não possua, crie uma.

### Passo 2

Crie uma função lambda com o nome `lambda_handler` que execute o `Python 3.9`.

### Passo 3

Crie seu bucket e adicione o arquivo CSV que você deseja inserir no banco.

### Passo 4

No painel Lambda, adicione o gatilho S3 à sua função.

### Passo 5

Crie seu banco no DynamoDB e adicione uma chave de partição do tipo String com o nome `ID_CESSAO`.

### Passo 6

Adicione as seguintes políticas à sua função Lambda:

#### Get Object (Libera o acesso ao arquivo CSV)
```bash
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucketcsvtestlambda/*"
        }
    ]
}
```

#### PutItem (Libera o acesso à escrita da função no banco)
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "*"
        }
    ]
}
```
### Passo 7

Copie o código do arquivo lambda_handler.py e cole na seção código do serviço Lambda da AWS. Em seguida, dê o deploy e execute o teste.


### Resultado do teste (OK)
```
Test Event Name
test_lambda_handler

Response
{
  "statusCode": 200,
  "body": "success",
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  }
}
```
