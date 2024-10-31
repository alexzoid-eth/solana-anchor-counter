## Program

```bash
avm use 0.29.0
anchor keys sync
anchor build
solana program deploy target/deploy/pda_local.so
```

## Scripts

- [client-gen](https://kevinheavey.github.io/anchorpy/clientgen/)

- install python requirements
```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
anchorpy client-gen ../target/idl/anchor_counter.json clientgen/ --program-id %PROGRAM_ID%
```