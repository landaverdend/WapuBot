import os
from wapu_cli.client import WapuClient, AuthContext
from wapu_cli.errors import WapuCLIError
from google.adk.tools import FunctionTool

WAPU_BASE_URL = os.environ.get("WAPU_API_BASE_URL", "https://be-prod.wapu.app")


def build_tools(wapu_api_key: str) -> list[FunctionTool]:
    client = WapuClient(base_url=WAPU_BASE_URL, auth=AuthContext(api_key=wapu_api_key))

    def get_balance() -> dict:
        """Get the user's current wallet balance and account info."""
        try:
            return client.get_home()
        except WapuCLIError as e:
            return {"error": str(e)}

    def get_transactions() -> dict:
        """List the user's recent transactions."""
        try:
            return client.list_transactions()
        except WapuCLIError as e:
            return {"error": str(e)}

    def get_lightning_address() -> dict:
        """Get the user's Lightning address (e.g. username@wapu.app)."""
        try:
            return client.get_lightning_address()
        except WapuCLIError as e:
            return {"error": str(e)}

    def create_lightning_invoice(amount: float, currency: str) -> dict:
        """
        Create a Lightning invoice so another party can pay the user.

        Args:
            amount: Amount to receive.
            currency: Currency code (e.g. 'USDT', 'BTC').
        """
        try:
            return client.create_lightning_deposit(amount=amount, currency=currency)
        except WapuCLIError as e:
            return {"error": str(e)}

    def send_to_username(amount: float, currency: str, receiver_username: str) -> dict:
        """
        Send funds to another Wapu user by their username.

        Args:
            amount: Amount to send.
            currency: Currency code (e.g. 'USDT', 'BTC').
            receiver_username: The recipient's Wapu username.
        """
        try:
            return client.create_inner_transfer(
                amount=amount, currency=currency, receiver_username=receiver_username
            )
        except WapuCLIError as e:
            return {"error": str(e)}

    def get_crypto_deposit_address(amount: float, currency: str, network: str) -> dict:
        """
        Get an on-chain deposit address to receive crypto.

        Args:
            amount: Amount to receive.
            currency: Currency code (e.g. 'USDT', 'BTC').
            network: Blockchain network (e.g. 'ETH', 'TRX', 'BTC').
        """
        try:
            return client.create_crypto_deposit(amount=amount, currency=currency, network=network)
        except WapuCLIError as e:
            return {"error": str(e)}

    def withdraw_crypto(address: str, network: str, currency: str, amount: float) -> dict:
        """
        Withdraw crypto to an external wallet address.

        Args:
            address: Destination wallet address.
            network: Blockchain network (e.g. 'ETH', 'TRX', 'BTC').
            currency: Currency code (e.g. 'USDT', 'BTC').
            amount: Amount to withdraw.
        """
        try:
            return client.create_crypto_withdrawal(
                address=address, network=network, currency=currency, amount=amount
            )
        except WapuCLIError as e:
            return {"error": str(e)}

    def list_contacts(filter_type: str | None = None) -> dict:
        """
        List the user's contacts.

        Args:
            filter_type: Optional filter (e.g. 'favourite').
        """
        try:
            return client.list_contacts(filter_type=filter_type)
        except WapuCLIError as e:
            return {"error": str(e)}

    def get_tentative_amount(
        amount: float, currency_payment: str, currency_taken: str, transaction_type: str
    ) -> dict:
        """
        Get a tentative conversion amount before executing a transaction. Useful for showing exchange rates.

        Args:
            amount: The amount to convert.
            currency_payment: The currency being paid out (e.g. 'USDT').
            currency_taken: The currency being received (e.g. 'ARS').
            transaction_type: Transaction type (e.g. 'TRANSFER', 'WITHDRAWAL').
        """
        try:
            return client.get_tentative_amount(
                amount=amount,
                currency_payment=currency_payment,
                currency_taken=currency_taken,
                transaction_type=transaction_type,
            )
        except WapuCLIError as e:
            return {"error": str(e)}

    return [
        FunctionTool(get_balance),
        FunctionTool(get_transactions),
        FunctionTool(get_lightning_address),
        FunctionTool(create_lightning_invoice),
        FunctionTool(send_to_username),
        FunctionTool(get_crypto_deposit_address),
        FunctionTool(withdraw_crypto),
        FunctionTool(list_contacts),
        FunctionTool(get_tentative_amount),
    ]
