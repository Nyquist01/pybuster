from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TargetHosts(Base):
    __tablename__ = "target_hosts"

    target_host_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    target_host: Mapped[str] = mapped_column(nullable=False)


class Scans(Base):
    __tablename__ = "scans"

    scan_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    target_host_id: Mapped[int] = mapped_column(
        ForeignKey("target_hosts.target_host_id")
    )
    scanned_at: Mapped[str]
    scan_status: Mapped[str]


class ScanResults(Base):
    __tablename__ = "scan_results"

    result_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.scan_id"))
    path: Mapped[str] = mapped_column(nullable=False)
    status_code: Mapped[int] = mapped_column(nullable=False)
    size: Mapped[int]
    content_type: Mapped[str]
    server: Mapped[str]
    tech: Mapped[str]
