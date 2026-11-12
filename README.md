# bambu-a1-acabamento

Skill de agente (formato [Agent Skills](https://agentskills.io): `SKILL.md` + scripts + referências) para preparar modelos 3D e imprimir na **Bambu Lab A1 (bico 0,4, AMS lite)** com o melhor acabamento: conversão de perfil de outra impressora, altura de camada medida no fatiador, suporte em figura, purga menor, conferência do G-code e pós-impressão.

*An agent skill (pt-BR) for high-quality prints on the Bambu Lab A1. Any LLM can use it: read `SKILL.md` first.*

## Como usar

| Agente | Instalação |
|---|---|
| Claude Code | `git clone https://github.com/RodrigoAlbe/bambu-a1-acabamento ~/.claude/skills/bambu-a1-acabamento` |
| Codex CLI e outros com Agent Skills | clone em `~/.agents/skills/` (ou na pasta de skills do agente) |
| Cursor, Gemini CLI, Copilot e agentes que leem `AGENTS.md` | clone dentro do projeto; o `AGENTS.md` aponta pro `SKILL.md` |
| Chat sem arquivos (ChatGPT, Claude.ai, Gemini) | cole o `SKILL.md` como instrução e anexe a referência que precisar |

## O que tem

- `SKILL.md`: o fluxo, o que foi medido e o que ainda falta testar.
- `scripts/`: conversão de 3MF para a A1, relatório de fatiamento, camada adaptativa, análise de suporte (pontas, troncos, contatos) e bloqueio de suporte no rosto.
- `references/`: pesquisa com fonte e data (vídeos, wikis, A/B impressos).
- `assets/`: configuração base do projeto para a A1.

## Requisitos dos scripts

macOS com Bambu Studio instalado (o CLI vem no app) e Python 3. O `makerworld.sh` baixa pelo Safari já logado no MakerWorld. Sem isso, a parte de texto da skill continua valendo.

## Avisos

- Números vêm do fatiador ou de impressão real, com data. O que está em "ainda falta teste" não foi impresso na A1.
- Nunca mande imprimir sozinho: o agente prepara o arquivo, a pessoa aperta Imprimir.

Licença MIT.
