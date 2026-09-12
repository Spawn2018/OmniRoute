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
from app.models.chassis_mark import ChassisMark  # noqa: F401
from app.models.line_impact_mark import LineImpactMark  # noqa: F401
from app.models.three_way_mark import ThreeWayMark  # noqa: F401

from app.models.commodity_code import CommodityCode  # noqa: F401
from app.models.credit_review import CreditReview  # noqa: F401
from app.models.dangerous_good import DangerousGood  # noqa: F401
from app.models.document_checklist_rule import DocumentChecklistRule  # noqa: F401
from app.models.document_dispatch_rule import DocumentDispatchRule  # noqa: F401
from app.models.booking_instruction import BookingInstruction  # noqa: F401
from app.models.field_carry_forward import FieldCarryForward  # noqa: F401
from app.models.inbound_message import InboundMessage  # noqa: F401
from app.models.incoterm_responsibility import IncotermResponsibility  # noqa: F401
from app.models.shipment_stakeholder import ShipmentStakeholder  # noqa: F401
from app.models.customer_rfq import CustomerRfq  # noqa: F401
from app.models.network import Network  # noqa: F401
from app.models.network_member import NetworkMember  # noqa: F401
from app.models.carrier_inquiry import CarrierInquiry  # noqa: F401
from app.models.nbp_rate import NbpRate  # noqa: F401
from app.models.rate_line import RateLine  # noqa: F401
from app.models.charge import Charge  # noqa: F401
from app.models.quotation import Quotation  # noqa: F401
from app.models.organization_calendar import OrganizationCalendar  # noqa: F401
from app.models.stop import Stop  # noqa: F401
from app.models.resource import Resource  # noqa: F401
from app.models.trip import Trip  # noqa: F401
from app.models.container import Container  # noqa: F401
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
from app.models.party_lane_scorecard import PartyLaneScorecard  # noqa: F401
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
from app.models.groupage_line import GroupageLine  # noqa: F401
from app.models.shipment_package import ShipmentPackage  # noqa: F401
from app.models.dock_appointment import DockAppointment  # noqa: F401
from app.models.cod_instruction import CodInstruction  # noqa: F401
from app.models.groupage_tariff import GroupageTariff  # noqa: F401
from app.models.ocean_bill import OceanBill  # noqa: F401
from app.models.consignment import Consignment  # noqa: F401
from app.models.pallet_balance import PalletBalance  # noqa: F401
from app.models.document_template import DocumentTemplate  # noqa: F401
from app.models.rate_card import RateCard  # noqa: F401
from app.models.charge_template import ChargeTemplate  # noqa: F401
from app.models.fuel_index import FuelIndex  # noqa: F401
from app.models.local_charge import LocalCharge  # noqa: F401
from app.models.tender_quote import TenderQuote  # noqa: F401
from app.models.tender import Tender  # noqa: F401
from app.models.tender_lot import TenderLot  # noqa: F401
from app.models.tender_lane import TenderLane  # noqa: F401
from app.models.tender_round import TenderRound  # noqa: F401
from app.models.tender_data_room import TenderDataRoom  # noqa: F401
from app.models.tender_matrix_cell import TenderMatrixCell  # noqa: F401
from app.models.tender_playbook import TenderPlaybook  # noqa: F401
from app.models.tender_consortium_member import TenderConsortiumMember  # noqa: F401
from app.models.tender_award_review import TenderAwardReview  # noqa: F401
from app.models.tender_bid_stance import TenderBidStance  # noqa: F401
from app.models.tender_carbon_mark import TenderCarbonMark  # noqa: F401
from app.models.lane_pattern import LanePattern  # noqa: F401
from app.models.kreptd_licence import KreptdLicence  # noqa: F401
from app.models.monitoring_scheme import MonitoringScheme  # noqa: F401
from app.models.party_document import PartyDocument  # noqa: F401
from app.models.carbon_method import CarbonMethod  # noqa: F401
from app.models.plan_snapshot import PlanSnapshot  # noqa: F401
from app.models.circle_sim import CircleSim  # noqa: F401
from app.models.lane_km import LaneKm  # noqa: F401
from app.models.erp_connector import ErpConnector  # noqa: F401
from app.models.customer_contract import CustomerContract  # noqa: F401
from app.models.tenant_contract_kek import TenantContractKek  # noqa: F401
from app.models.visibility_connector import VisibilityConnector  # noqa: F401
from app.models.purchase_order import PurchaseOrder  # noqa: F401
from app.models.po_line import PoLine  # noqa: F401
from app.models.asn import Asn  # noqa: F401
from app.models.otif_mark import OtifMark  # noqa: F401
from app.models.sap_connector import SapConnector  # noqa: F401
from app.models.capa_mark import CapaMark  # noqa: F401
from app.models.spend_mark import SpendMark  # noqa: F401
from app.models.penalty_mark import PenaltyMark  # noqa: F401
from app.models.intervention_outcome import InterventionOutcome  # noqa: F401
from app.models.crm_lead import CrmLead  # noqa: F401
from app.models.lc_checklist import LcChecklist  # noqa: F401
from app.models.ncts_draft import NctsDraft  # noqa: F401
from app.models.oog_mark import OogMark  # noqa: F401
from app.models.load_plan_mark import LoadPlanMark  # noqa: F401
from app.models.cmms_mark import CmmsMark  # noqa: F401
from app.models.legal_hold_mark import LegalHoldMark  # noqa: F401
from app.models.company_mark import CompanyMark  # noqa: F401
from app.models.bonded_mark import BondedMark  # noqa: F401
from app.models.filing_scheme_mark import FilingSchemeMark  # noqa: F401
from app.models.edi_map_mark import EdiMapMark  # noqa: F401
from app.models.aeo_dossier_mark import AeoDossierMark  # noqa: F401
from app.models.yard_mark import YardMark  # noqa: F401
from app.models.billing_mark import BillingMark  # noqa: F401
from app.models.registry_poll_mark import RegistryPollMark  # noqa: F401
from app.models.working_capital_mark import WorkingCapitalMark  # noqa: F401
from app.models.make_or_buy_mark import MakeOrBuyMark  # noqa: F401
from app.models.cost_allocation_mark import CostAllocationMark  # noqa: F401
from app.models.cargo_cover_mark import CargoCoverMark  # noqa: F401
from app.models.sanctions_mark import SanctionsMark  # noqa: F401
from app.models.subcontract_edge_mark import SubcontractEdgeMark  # noqa: F401
from app.models.schedule_exception_mark import ScheduleExceptionMark  # noqa: F401
from app.models.cutoff_mark import CutoffMark  # noqa: F401
from app.models.time_to_fix_mark import TimeToFixMark  # noqa: F401
from app.models.what_if_mark import WhatIfMark  # noqa: F401
from app.models.cabotage_mark import CabotageMark  # noqa: F401
from app.models.combined_transport_mark import CombinedTransportMark  # noqa: F401
from app.models.ferry_art9_mark import FerryArt9Mark  # noqa: F401
from app.models.fuel_anomaly_mark import FuelAnomalyMark  # noqa: F401
from app.models.fuel_card_mark import FuelCardMark  # noqa: F401
from app.models.fleet_cost_mark import FleetCostMark  # noqa: F401
from app.models.bin_pack_mark import BinPackMark  # noqa: F401
from app.models.pallet_pool_mark import PalletPoolMark  # noqa: F401
from app.models.e_cmr_mark import ECmrMark  # noqa: F401
from app.models.e_delivery_mark import EDeliveryMark  # noqa: F401
from app.models.e_doreczenia_mark import EDoreczeniaMark  # noqa: F401
from app.models.peppol_mark import PeppolMark  # noqa: F401
from app.models.sid_import_mark import SidImportMark  # noqa: F401
from app.models.integration_hub_mark import IntegrationHubMark  # noqa: F401
from app.models.webhook_outbox_mark import WebhookOutboxMark  # noqa: F401
from app.models.partner_exchange_mark import PartnerExchangeMark  # noqa: F401
from app.models.regulatory_radar_mark import RegulatoryRadarMark  # noqa: F401
from app.models.iso_nis2_mark import IsoNis2Mark  # noqa: F401
from app.models.offboarding_mark import OffboardingMark  # noqa: F401
from app.models.jit_jis_mark import JitJisMark  # noqa: F401
from app.models.vda_odette_mark import VdaOdetteMark  # noqa: F401
from app.models.inventory_position_mark import InventoryPositionMark  # noqa: F401
from app.models.fair_share_mark import FairShareMark  # noqa: F401
from app.models.mqc_mark import MqcMark  # noqa: F401
from app.models.eccn_mark import EccnMark  # noqa: F401
from app.models.eur1_atr_mark import Eur1AtrMark  # noqa: F401
from app.models.phyto_ata_mark import PhytoAtaMark  # noqa: F401
from app.models.switch_bl_loi_mark import SwitchBlLoiMark  # noqa: F401
from app.models.abandoned_rto_mark import AbandonedRtoMark  # noqa: F401
from app.models.general_average_mark import GeneralAverageMark  # noqa: F401
from app.models.tender_decline_reason import TenderDeclineReason  # noqa: F401
from app.models.demand_snapshot_mark import DemandSnapshotMark  # noqa: F401
from app.models.demo_gps_mark import DemoGpsMark  # noqa: F401
from app.models.demo_sim_mark import DemoSimMark  # noqa: F401
from app.models.demo_wipe_mark import DemoWipeMark  # noqa: F401
from app.models.dual_ledger_mark import DualLedgerMark  # noqa: F401
from app.models.po_plant_mark import PoPlantMark  # noqa: F401
from app.models.po_sku_mark import PoSkuMark  # noqa: F401
from app.models.po_batch_mark import PoBatchMark  # noqa: F401
from app.models.un_segregation_mark import UnSegregationMark  # noqa: F401
from app.models.impersonate_guard_mark import ImpersonateGuardMark  # noqa: F401
from app.models.csrd_mark import CsrdMark  # noqa: F401

from app.models.air_ra3_mark import AirRa3Mark  # noqa: F401
from app.models.rail_cim_mark import RailCimMark  # noqa: F401
from app.models.rail_uic_mark import RailUicMark  # noqa: F401
from app.models.ocean_alliance_mark import OceanAllianceMark  # noqa: F401
from app.models.ocean_feeder_mark import OceanFeederMark  # noqa: F401
from app.models.reefer_mark import ReeferMark  # noqa: F401
from app.models.empty_depot_mark import EmptyDepotMark  # noqa: F401
from app.models.nvocc_mark import NvoccMark  # noqa: F401
from app.models.multi_manning_mark import MultiManningMark  # noqa: F401
from app.models.posting_mark import PostingMark  # noqa: F401
from app.models.tacho_office_mark import TachoOfficeMark  # noqa: F401
from app.models.lez_mark import LezMark  # noqa: F401
from app.models.label_parking_mark import LabelParkingMark  # noqa: F401
from app.models.ab_sus_mark import AbSusMark  # noqa: F401
from app.models.funnel_mark import FunnelMark  # noqa: F401
from app.models.terms_ai_mark import TermsAiMark  # noqa: F401
from app.models.mail_accept_mark import MailAcceptMark  # noqa: F401
from app.models.role_view_mark import RoleViewMark  # noqa: F401
from app.models.rag_sop_mark import RagSopMark  # noqa: F401
from app.models.copy_ban_mark import CopyBanMark  # noqa: F401
from app.models.erru_mark import ErruMark  # noqa: F401
from app.models.job_metric_mark import JobMetricMark  # noqa: F401
from app.models.mobile_client_mark import MobileClientMark  # noqa: F401
from app.models.collaboration_mark import CollaborationMark  # noqa: F401
from app.models.freight_audit_mark import FreightAuditMark  # noqa: F401
from app.models.routing_guide import RoutingGuide  # noqa: F401
from app.models.routing_guide_enforcement import RoutingGuideEnforcement  # noqa: F401
from app.models.routing_guide_match import RoutingGuideMatch  # noqa: F401
from app.models.exchange_connector import ExchangeConnector  # noqa: F401
from app.models.idp_connector import IdpConnector  # noqa: F401
from app.models.terminal_slot_connector import TerminalSlotConnector  # noqa: F401
from app.models.prediction_ledger import PredictionLedger  # noqa: F401
from app.models.weather_observation import WeatherObservation  # noqa: F401
from app.models.free_time_clock import FreeTimeClock  # noqa: F401
from app.models.telematics_connector import TelematicsConnector  # noqa: F401
from app.models.tower_impact import TowerImpact  # noqa: F401
from app.models.twin_mark import TwinMark  # noqa: F401
from app.models.war_room_mark import WarRoomMark  # noqa: F401
from app.models.memory_edge import MemoryEdge  # noqa: F401
from app.models.executive_mark import ExecutiveMark  # noqa: F401
from app.models.rank_mark import RankMark  # noqa: F401
from app.models.task_template import TaskTemplate  # noqa: F401
from app.models.cash_discount import CashDiscount  # noqa: F401
from app.models.tender_ted_notice import TenderTedNotice  # noqa: F401
from app.models.tender_prospect import TenderProspect  # noqa: F401
from app.models.tender_rfp_intake import TenderRfpIntake  # noqa: F401
from app.models.tender_win_loss import TenderWinLoss  # noqa: F401
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
