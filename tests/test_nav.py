import yaml
with open("mkdocs.yml", "r") as f:
    config = yaml.safe_load(f)

config["plugins"] = ["awesome-pages"]
config["nav"] = [
    {"Welcome": "index.md"},
    {"Core Strategy": "docs/core"},
    {"Technical Architecture": "docs/technical"},
    {"Operations & Runbooks": "docs/operations"},
    {"Quality Assurance": "docs/qa"},
    {"Agent Ecosystem": "agents"}
]

with open("mkdocs_new.yml", "w") as f:
    yaml.dump(config, f, sort_keys=False)
