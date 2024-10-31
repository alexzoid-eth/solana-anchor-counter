## Program

```bash
avm use 0.29.0
anchor build
anchor keys sync
solana program deploy target/deploy/pda_local.so
```

## App

- anchorpy directory was generated with [client-gen](https://kevinheavey.github.io/anchorpy/clientgen/)
```bash
anchorpy client-gen ../target/idl/anchor_counter.json anchorpy/ --program-id 82yvAmHLc7dQz5XgPp2XByY7dBpLL1GhZtXhNbQ5RL2y
```

- install python requirements
```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- set `PROGRAM_ID` in `anchorpy\program_id.py`