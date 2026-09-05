# Plugins do KeyTune

Catálogo público usado pelo marketplace do KeyTune 2. O player consulta `catalog.json` na branch `main`.

## Instalar

No gerenciador de plugins do KeyTune, escolha **Abrir marketplace**, selecione o plugin e confirme os dados e permissões apresentados. Também é possível baixar um arquivo `.ktplugin` nas Releases e instalá-lo pelo gerenciador.

Plugins são código Python com acesso ao computador. Instale apenas plugins de autores em quem você confia. O processo separado isola falhas comuns, mas não é uma sandbox de segurança.

## Contribuir

1. Crie seu plugin seguindo o [guia de desenvolvimento](https://github.com/Ed-Fe/KeyTune/blob/main/docs/plugins.md).
2. Publique o pacote `.ktplugin` em uma Release pública do seu repositório.
3. Calcule o SHA-256 do arquivo final; no PowerShell: `Get-FileHash arquivo.ktplugin -Algorithm SHA256`.
4. Abra uma pull request adicionando ou atualizando uma entrada em `catalog.json`, com id, nome, versão, descrição, autor, homepage, URL HTTPS do pacote, SHA-256 em minúsculas e `verified: false`.
5. Aguarde a validação automática e a revisão de um mantenedor.

Publique uma nova versão quando alterar um pacote. Não substitua arquivos já catalogados. Cada id aparece apenas uma vez no catálogo, apontando para a versão distribuída atualmente.

O campo `verified` é reservado aos mantenedores após revisão humana da procedência; não representa uma garantia de segurança. A automação verifica schema, ids únicos, download, checksum, caminhos do ZIP, manifesto, entrypoint e compatibilidade com a versão de referência do KeyTune. Ela não executa o plugin.

## Manutenção

O workflow fixa o código do KeyTune em um commit revisado. Atualize essa referência quando o contrato suportado mudar. Alterações no workflow e no validador também exigem revisão dos mantenedores.

Para validar localmente, instale `jsonschema` e execute `python scripts/validate_catalog.py --keytune ../Media-Player`. O comando baixa os pacotes e os instala somente em diretórios temporários, sem ativá-los.
