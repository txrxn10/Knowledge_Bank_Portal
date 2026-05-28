from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class ApprovalWorkflow(BaseModel):
    __tablename__ = "approval_workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(9), nullable=False)
    initiated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    current_step = Column(Integer, nullable=False)
    total_steps = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    completed_at = Column(String, nullable=True)


class ApprovalStep(BaseModel):
    __tablename__ = "approval_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("approval_workflows.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(14), nullable=False)
    decision_notes = Column(String, nullable=True)
    decided_at = Column(String, nullable=True)
