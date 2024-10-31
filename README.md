Example from Solana Anchor [Onchain Development](https://solana.com/developers/courses/onchain-development) course.

## Program

```bash
avm use 0.29.0
anchor keys sync
anchor build
solana program deploy target/deploy/anchor_counter.so
```

## Scripts

[client-gen](https://kevinheavey.github.io/anchorpy/clientgen/) generates a Python client based on an Anchor IDL. Change `%PROGRAM_ID%` with deployed program id.
```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
anchorpy client-gen ../target/idl/anchor_counter.json clientgen/ --program-id %PROGRAM_ID%
python main.py
```
