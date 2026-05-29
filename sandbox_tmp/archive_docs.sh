#!/bin/bash

# Ensure archive directories exist
mkdir -p docs/archive/core
mkdir -p docs/archive/technical
mkdir -p docs/archive/operations
mkdir -p docs/archive/qa

# Move superseded/epic files from docs/core
mv docs/core/epic_project_scope_remediation.md docs/archive/core/ 2>/dev/null
mv docs/core/infrastructure_remediation_prd.md docs/archive/core/ 2>/dev/null
mv docs/core/infrastructure_remediation_sprint_plan.md docs/archive/core/ 2>/dev/null
mv docs/core/Phase_3_Rebuild_Master_Plan.md docs/archive/core/ 2>/dev/null
mv docs/core/phase_4_master_plan.md docs/archive/core/ 2>/dev/null
mv docs/core/phase_4_reassessment_strategy.md docs/archive/core/ 2>/dev/null
mv docs/core/phase_5_master_plan.md docs/archive/core/ 2>/dev/null
mv docs/core/prd_epic_4.4.C_e2e_pod_testing.md docs/archive/core/ 2>/dev/null
mv docs/core/prd_epic_5.1.A_gtm_strategy.md docs/archive/core/ 2>/dev/null
mv docs/core/prd_epic_custom_agent_remediation.md docs/archive/core/ 2>/dev/null
mv docs/core/prd_phase_3_rebuild.md docs/archive/core/ 2>/dev/null
mv docs/core/prd_phase_5.md docs/archive/core/ 2>/dev/null
mv docs/core/Launch_Blog_Post.md docs/archive/core/ 2>/dev/null

# Move superseded/epic files from docs/technical
mv docs/technical/agent_format_prpm_evaluation.md docs/archive/technical/ 2>/dev/null
mv docs/technical/api_architecture_options.md docs/archive/technical/ 2>/dev/null
mv docs/technical/backend_assessment_phase_4.md docs/archive/technical/ 2>/dev/null
mv docs/technical/core_ui_evaluation_report.md docs/archive/technical/ 2>/dev/null
mv docs/technical/design_plans_review_report.md docs/archive/technical/ 2>/dev/null
mv docs/technical/eng_spec_phase_3_rebuild.md docs/archive/technical/ 2>/dev/null
mv docs/technical/epic_4.4.C_technical_design.md docs/archive/technical/ 2>/dev/null
mv docs/technical/epic_custom_agent_remediation_plan.md docs/archive/technical/ 2>/dev/null
mv docs/technical/epic_custom_agent_remediation_tech_design.md docs/archive/technical/ 2>/dev/null
mv docs/technical/phase_2_automated_scoping_spec.md docs/archive/technical/ 2>/dev/null
mv docs/technical/phase_5_technical_design.md docs/archive/technical/ 2>/dev/null
mv docs/technical/semantic_storage_evaluation.md docs/archive/technical/ 2>/dev/null
mv docs/technical/sprint_4.1_backend_architecture.md docs/archive/technical/ 2>/dev/null
mv docs/technical/sprint_4.2_semantic_memory_spec.md docs/archive/technical/ 2>/dev/null
mv docs/technical/sprint_4.3_frontend_marketplace_spec.md docs/archive/technical/ 2>/dev/null
mv docs/technical/ux_assessment_phase_4.md docs/archive/technical/ 2>/dev/null
mv docs/technical/intro_page_redesign_plan.md docs/archive/technical/ 2>/dev/null
mv docs/technical/mobile_ui_design_plan.md docs/archive/technical/ 2>/dev/null
mv docs/technical/global_design_system_plan.md docs/archive/technical/ 2>/dev/null
mv docs/technical/chat_scope_interface_redesign.md docs/archive/technical/ 2>/dev/null
mv docs/technical/sidebar_menu_structure_analysis.md docs/archive/technical/ 2>/dev/null

# Move superseded/epic files from docs/operations
mv docs/operations/building_agency_os.md docs/archive/operations/ 2>/dev/null
mv docs/operations/community_engagement_log_5.2.C.md docs/archive/operations/ 2>/dev/null
mv docs/operations/compliance_signoff_custom_agent_remediation.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Content_Staging_Pipeline.md docs/archive/operations/ 2>/dev/null
mv docs/operations/context_audit_findings.md docs/archive/operations/ 2>/dev/null
mv docs/operations/context_board_review.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Cross_Channel_Activation_Strategy.md docs/archive/operations/ 2>/dev/null
mv docs/operations/deployment_log_5.2.A.md docs/archive/operations/ 2>/dev/null
mv docs/operations/devops_assessment_phase_4.md docs/archive/operations/ 2>/dev/null
mv docs/operations/devops_storage_migration_spec.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Executive_Summary_Report.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Executive_Workspace_Health_Deck.md docs/archive/operations/ 2>/dev/null
mv docs/operations/housekeeping_report.md docs/archive/operations/ 2>/dev/null
mv docs/operations/marketing_activation_log_5.2.B.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Phase_1_and_2_Reassessment_Report.md docs/archive/operations/ 2>/dev/null
mv docs/operations/phase_3_qa_notes.md docs/archive/operations/ 2>/dev/null
mv docs/operations/phase_3_reassessment_report.md docs/archive/operations/ 2>/dev/null
mv docs/operations/phase_3_tech_notes.md docs/archive/operations/ 2>/dev/null
mv docs/operations/phase_4_5_strategic_audit.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Pitch_Document.md docs/archive/operations/ 2>/dev/null
mv docs/operations/post_launch_synthesis_sprint_5.3.md docs/archive/operations/ 2>/dev/null
mv docs/operations/Sales_One_Pager_and_Battlecards.md docs/archive/operations/ 2>/dev/null
mv docs/operations/sprint_plan_phase_3_rebuild.md docs/archive/operations/ 2>/dev/null
mv docs/operations/ui_copy_update_plan.md docs/archive/operations/ 2>/dev/null
mv docs/operations/validation_impact_assessment.md docs/archive/operations/ 2>/dev/null
mv docs/operations/workspace_assessment_findings.md docs/archive/operations/ 2>/dev/null
mv docs/operations/workspace_health_presentation.html docs/archive/operations/ 2>/dev/null
mv docs/operations/workspace_health_summary.md docs/archive/operations/ 2>/dev/null

# Clean up any files dropped in the root of docs/archive instead of their subfolders
find docs/archive -maxdepth 1 -name "*.md" -type f -exec mv {} docs/archive/core/ \;

echo "Archiving complete"
# Move superseded/epic files from docs/qa
mv docs/qa/application_audit_report.md docs/archive/qa/ 2>/dev/null
mv docs/qa/architectural_remediation_assessment_v2.md docs/archive/qa/ 2>/dev/null
mv docs/qa/architectural_review.md docs/archive/qa/ 2>/dev/null
mv docs/qa/audit_plan.md docs/archive/qa/ 2>/dev/null
mv docs/qa/backend_audit_report.md docs/archive/qa/ 2>/dev/null
mv docs/qa/custom_agent_error_resolution_log.md docs/archive/qa/ 2>/dev/null
mv docs/qa/custom_agent_tenant_isolation_qa_signoff.md docs/archive/qa/ 2>/dev/null
mv docs/qa/epic_1_sprint_1_qa_signoff.md docs/archive/qa/ 2>/dev/null
mv docs/qa/frontend_audit_report.md docs/archive/qa/ 2>/dev/null
mv docs/qa/hitl_instructions_epic_4.4.B.md docs/archive/qa/ 2>/dev/null
mv docs/qa/hitl_instructions_epic_4.4.C.md docs/archive/qa/ 2>/dev/null
mv docs/qa/hitl_instructions_epic_custom_agent_remediation_phase2.md docs/archive/qa/ 2>/dev/null
mv docs/qa/phase_5_compliance_signoff.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_gates_phase_3_rebuild.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_log_epic_a.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_epic_4.4.C.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_epic_project_scope_remediation.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_phase_3_custom_agent_remediation.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_phase_4_epic_4.4.A.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_phase_4_sprint_4_1.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_sprint_4_sandbox.md docs/archive/qa/ 2>/dev/null
mv docs/qa/qa_signoff_ticket_2.2.md docs/archive/qa/ 2>/dev/null
mv docs/qa/sprint_4.2_semantic_memory_qa.md docs/archive/qa/ 2>/dev/null
mv docs/qa/sprint_4.3_frontend_marketplace_qa.md docs/archive/qa/ 2>/dev/null
mv docs/qa/test_plan_custom_agent_remediation.md docs/archive/qa/ 2>/dev/null
mv docs/qa/test_plan_epic_4.4.C.md docs/archive/qa/ 2>/dev/null
mv docs/qa/test_plan_phase_5.md docs/archive/qa/ 2>/dev/null
