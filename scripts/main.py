from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.keypair import Keypair
from solana.rpc.commitment import Confirmed
import json
import os

# Import our generated code
from clientgen.program_id import PROGRAM_ID
from clientgen.accounts.counter import Counter
from clientgen.instructions.initialize import initialize
from clientgen.instructions.increment import increment
from solana.rpc.core import RPCException
from clientgen.errors.anchor import from_code

async def main():
    # Setup client - connecting to devnet
    client = AsyncClient("https://api.devnet.solana.com", commitment=Confirmed)
    
    # Load wallet from JSON file
    with open("/home/zoid/.config/solana/id.json", 'r') as f:
        keypair_data = json.load(f)
    payer = Keypair.from_bytes(bytes(keypair_data))
    
    print(f"Using account: {payer.pubkey()}")
    
    try:
        # Get account balance
        balance = await client.get_balance(payer.pubkey())
        print(f"Account balance: {balance.value/1e9} SOL")

        # Create a new keypair for the counter account
        counter_keypair = Keypair()
        print(f"Counter account: {counter_keypair.pubkey()}")
        
        # Initialize counter account
        init_ix = initialize(
            {
                "counter": counter_keypair.pubkey(),
                "user": payer.pubkey(),
            }
        )
        
        init_tx = Transaction().add(init_ix)
        
        print("Initializing counter account...")
        
        # Get recent blockhash
        recent_blockhash = await client.get_latest_blockhash()
        init_tx.recent_blockhash = recent_blockhash.value.blockhash
        
        # Set fee payer
        init_tx.fee_payer = payer.pubkey()
        
        # Sign transaction
        init_tx.sign(payer, counter_keypair)
        
        # Send raw transaction
        init_sig = await client.send_raw_transaction(init_tx.serialize())
        print(f"Transaction signature: {init_sig.value}")
        
        # Wait for confirmation
        await client.confirm_transaction(init_sig.value)
        
        # Fetch the counter account data
        counter = await Counter.fetch(
            client,
            counter_keypair.pubkey()
        )
        
        print(f"Counter initialized. Current count: {counter.count}")
        
        # Increment counter
        inc_ix = increment(
            {
                "counter": counter_keypair.pubkey(),
                "user": payer.pubkey(),
            }
        )
        
        inc_tx = Transaction().add(inc_ix)
        
        print("Incrementing counter...")
        
        # Get recent blockhash for increment transaction
        recent_blockhash = await client.get_latest_blockhash()
        inc_tx.recent_blockhash = recent_blockhash.value.blockhash
        
        # Set fee payer
        inc_tx.fee_payer = payer.pubkey()
        
        # Sign increment transaction
        inc_tx.sign(payer)
        
        # Send raw transaction
        inc_sig = await client.send_raw_transaction(inc_tx.serialize())
        print(f"Transaction signature: {inc_sig.value}")
        
        # Wait for confirmation
        await client.confirm_transaction(inc_sig.value)
        
        # Fetch updated counter value
        counter = await Counter.fetch(
            client,
            counter_keypair.pubkey()
        )
        
        print(f"Counter incremented. New count: {counter.count}")
        
        await client.close()
        
    except RPCException as e:
        error = from_code(e.code)
        if error:
            print(f"Error: {error.msg}")
        else:
            print(f"Unknown error: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())