"""Solana Perps smart contract information module."""

import logging
import asyncio
import requests
from datetime import datetime
from typing import Dict, Optional, Any
import json

logger = logging.getLogger(__name__)

class PerpsContractInfo:
    """Handler for Solana perpetuals smart contract information."""
    
    def __init__(self):
        self.contract_id = "7VwAnHYuF5JCXhT9tLWNnbuD6buox8dPCpk7qBrMu3PA"
        self.solana_rpc_url = "https://api.devnet.solana.com"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
    
    async def get_contract_info(self) -> Dict[str, Any]:
        """Fetch smart contract information from Solana devnet."""
        try:
            # Check cache first
            cache_key = f"contract_{self.contract_id}"
            now = datetime.now().timestamp()
            
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if now - timestamp < self.cache_duration:
                    logger.info("Returning cached contract data")
                    return cached_data
            
            logger.info(f"Fetching fresh data for contract {self.contract_id}")
            
            # Fetch account info from Solana RPC
            account_info = await self._get_account_info()
            
            # Prepare the response data
            contract_data = {
                'contract_id': self.contract_id,
                'network': 'Solana Devnet',
                'account_info': account_info,
                'timestamp': datetime.now().isoformat(),
                'explorer_url': f"https://explorer.solana.com/address/{self.contract_id}?cluster=devnet"
            }
            
            # Cache the result
            self.cache[cache_key] = (contract_data, now)
            
            return contract_data
                
        except Exception as e:
            logger.error(f"Error fetching contract info: {e}")
            # Return basic info if API fails
            return {
                'contract_id': self.contract_id,
                'network': 'Solana Devnet',
                'error': 'Failed to fetch live data',
                'explorer_url': f"https://explorer.solana.com/address/{self.contract_id}?cluster=devnet",
                'timestamp': datetime.now().isoformat()
            }
    
    async def _get_account_info(self) -> Dict[str, Any]:
        """Get account information from Solana RPC."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                self.contract_id,
                {
                    "encoding": "base64",
                    "commitment": "confirmed"
                }
            ]
        }
        
        try:
            # Run requests in a thread since it's blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    self.solana_rpc_url,
                    json=payload,
                    timeout=10,
                    headers={'Content-Type': 'application/json'}
                )
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result')
                
                if result and result.get('value'):
                    account_value = result['value']
                    return {
                        'exists': True,
                        'lamports': account_value.get('lamports', 0),
                        'owner': account_value.get('owner'),
                        'executable': account_value.get('executable', False),
                        'rent_epoch': account_value.get('rentEpoch'),
                        'data_size': len(account_value.get('data', [''])[0]) if account_value.get('data') else 0
                    }
                else:
                    return {'exists': False, 'error': 'Account not found'}
            else:
                return {'exists': False, 'error': f'RPC error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error in RPC request: {e}")
            return {'exists': False, 'error': f'Request failed: {str(e)}'}
    
    def format_contract_message(self, contract_data: Dict[str, Any]) -> str:
        """Format contract information into a readable message."""
        try:
            contract_id = contract_data['contract_id']
            network = contract_data['network']
            explorer_url = contract_data['explorer_url']
            timestamp = contract_data['timestamp']
            
            message_parts = [
                "🔗 **Perpetuals Smart Contract Info**",
                "",
                f"**Program ID:** `{contract_id}`",
                f"**Network:** {network}",
                ""
            ]
            
            if 'error' in contract_data:
                message_parts.extend([
                    f"⚠️ **Status:** {contract_data['error']}",
                    "",
                    "The contract data could not be fetched from the RPC, but you can view it directly on the explorer."
                ])
            else:
                account_info = contract_data.get('account_info', {})
                
                if account_info.get('exists'):
                    lamports = account_info.get('lamports', 0)
                    sol_balance = lamports / 1_000_000_000  # Convert lamports to SOL
                    
                    message_parts.extend([
                        "✅ **Status:** Active on Devnet",
                        f"**Balance:** {sol_balance:.9f} SOL ({lamports:,} lamports)",
                        f"**Owner Program:** `{account_info.get('owner', 'Unknown')}`",
                        f"**Executable:** {'Yes' if account_info.get('executable') else 'No'}",
                        f"**Data Size:** {account_info.get('data_size', 0):,} bytes",
                        f"**Rent Epoch:** {account_info.get('rent_epoch', 'Unknown')}",
                        ""
                    ])
                else:
                    message_parts.extend([
                        "❌ **Status:** Account not found or inactive",
                        ""
                    ])
            
            message_parts.extend([
                "🔍 **Explorer Links:**",
                f"[View on Solana Explorer]({explorer_url})"
            ])
            
            return "\n".join(message_parts)
            
        except Exception as e:
            logger.error(f"Error formatting contract message: {e}")
            return (
                "🔗 **Perpetuals Smart Contract Info**\n\n"
                f"**Program ID:** `{self.contract_id}`\n"
                f"**Network:** Solana Devnet\n\n"
                f"❌ Error formatting data: {str(e)}\n\n"
                f"🔍 [View on Explorer](https://explorer.solana.com/address/{self.contract_id}?cluster=devnet)"
            )

# Global instance
perps_info = PerpsContractInfo()

async def get_perps_info() -> str:
    """Get formatted perpetuals contract information."""
    try:
        contract_data = await perps_info.get_contract_info()
        return perps_info.format_contract_message(contract_data)
    except Exception as e:
        logger.error(f"Error in get_perps_info: {e}")
        return (
            "🔗 **Perpetuals Smart Contract Info**\n\n"
            f"**Program ID:** `7VwAnHYuF5JCXhT9tLWNnbuD6buox8dPCpk7qBrMu3PA`\n"
            f"**Network:** Solana Devnet\n\n"
            f"❌ Unable to fetch contract data: {str(e)}\n\n"
            "🔍 [View on Explorer](https://explorer.solana.com/address/7VwAnHYuF5JCXhT9tLWNnbuD6buox8dPCpk7qBrMu3PA?cluster=devnet)"
        )