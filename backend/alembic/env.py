"""Generic single-database configuration."""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.models.app_user import AppUser  # noqa: F401
from app.models.base import Base
from app.models.organization import Organization  # noqa: F401
from app.models.charge_code import ChargeCode  # noqa: F401
from app.models.channel_quote import ChannelQuote  # noqa: F401
from app.models.commodity_code import CommodityCode  # noqa: F401
from app.models.credit_review import CreditReview  # noqa: F401
from app.models.dangerous_good import DangerousGood  # noqa: F401
from app.models.inbound_message import InboundMessage  # noqa: F401
from app.models.customer_rfq import CustomerRfq  # noqa: F401
from app.models.network import Network  # noqa: F401
from app.models.network_member import NetworkMember  # noqa: F401
from app.models.carrier_inquiry import CarrierInquiry  # noqa: F401
from app.models.nbp_rate import NbpRate  # noqa: F401
from app.models.rate_line import RateLine  # noqa: F401
from app.models.charge import Charge  # noqa: F401
from app.models.quotation import Quotation  # noqa: F401
from app.models.organization_setting import OrganizationSetting  # noqa: F401
from app.models.extraction_draft import ExtractionDraft  # noqa: F401
from app.models.table_view import TableView  # noqa: F401
from app.models.port import Port  # noqa: F401
from app.models.location import Location, LocationZoneMember  # noqa: F401
from app.models.terminal import Terminal  # noqa: F401
from app.models.party import Party  # noqa: F401
from app.models.party_contact import PartyContact  # noqa: F401
from app.models.party_bank_account import PartyBankAccount  # noqa: F401
from app.models.party_email_domain import PartyEmailDomain  # noqa: F401
from app.models.party_charge_override import PartyChargeOverride  # noqa: F401
from app.models.carrier_profile import CarrierProfile  # noqa: F401
from app.models.party_scorecard import PartyScorecard  # noqa: F401
from app.models.customer_sop import CustomerSop  # noqa: F401
from app.models.port_surcharge import PortSurcharge  # noqa: F401
from app.models.operator_decision import OperatorDecision  # noqa: F401
from app.models.operator_notice import OperatorNotice  # noqa: F401
from app.models.mail_draft import MailDraft  # noqa: F401
from app.models.outbox_event import OutboxEvent  # noqa: F401
from app.models.shipment import Shipment  # noqa: F401
from app.models.tracking_event import TrackingEvent  # noqa: F401
from app.models.shipment_document import ShipmentDocument  # noqa: F401
from app.models.operational_exception import OperationalException  # noqa: F401
from app.models.cargo_claim import CargoClaim  # noqa: F401
from app.models.fraud_flag import FraudFlag  # noqa: F401
from app.models.edi_message import EdiMessage  # noqa: F401
from app.models.sales_invoice import SalesInvoice  # noqa: F401
from app.models.bank_payment import BankPayment  # noqa: F401
from app.models.fx_difference import FxDifference  # noqa: F401
from app.models.cash_flow import CashFlow  # noqa: F401
from app.models.cost_to_serve import CostToServe  # noqa: F401
from app.models.bookkeeping import Bookkeeping  # noqa: F401
from app.models.collective_invoice import CollectiveInvoice  # noqa: F401
from app.models.gdpr_request import GdprRequest  # noqa: F401
from app.models.shipment_leg import ShipmentLeg  # noqa: F401
from app.models.money_cost import MoneyCost  # noqa: F401
from app.models.quote_invoice_settlement import QuoteInvoiceSettlement  # noqa: F401

config = context.config
# Testy nadpisują URL na omniroute_test. Domyślnie owner z settings — nie runtime omniroute_app.
config.set_main_option(
    "sqlalchemy.url",
    os.environ.get("ALEMBIC_DATABASE_URL") or settings.database_url_sync,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
