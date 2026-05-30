#!/bin/bash

# Ensure directories exist
mkdir -p docs/core/AgencyOS-Lite
mkdir -p docs/technical/AgencyOS-Lite
mkdir -p docs/operations/AgencyOS-Retrospective
mkdir -p docs/core/AgencyOS-vs-Copilots
mkdir -p docs/core/kinetik-os-analysis
mkdir -p docs/technical/kinetik-os-analysis
mkdir -p docs/operations/kinetik-os-analysis
mkdir -p docs/core/twin_so_analysis/v1
mkdir -p docs/technical/twin_so_analysis/v1
mkdir -p docs/core/twin_so_analysis/v2
mkdir -p docs/technical/twin_so_analysis/v2
mkdir -p docs/operations/twin_so_analysis/v2
mkdir -p docs/qa/twin_so_analysis/v2

# Move general research files
mv docs/research/Competitive_Analysis.md docs/core/Competitive_Analysis.md
mv docs/research/dependency_audit_report.md docs/technical/dependency_audit_report.md
mv docs/research/Feasibility_Studies.md docs/core/Feasibility_Studies.md
mv docs/research/Market_Trends_and_Opportunities.md docs/core/Market_Trends_and_Opportunities.md
mv docs/research/Regulatory_and_Compliance_Research.md docs/operations/Regulatory_and_Compliance_Research.md
mv docs/research/User_Insights_and_Personas.md docs/core/User_Insights_and_Personas.md

# AgencyOS-Lite
mv docs/research/AgencyOS-Lite/Market_and_Competitor_Analysis.md docs/core/AgencyOS-Lite/Market_and_Competitor_Analysis.md
mv docs/research/AgencyOS-Lite/Original_Repo_Usage.md docs/technical/AgencyOS-Lite/Original_Repo_Usage.md
mv docs/research/AgencyOS-Lite/Product_Exploration_Lite.md docs/core/AgencyOS-Lite/Product_Exploration_Lite.md

# AgencyOS-Retrospective
mv docs/research/AgencyOS-Retrospective/reusable_assets_and_learnings.md docs/operations/AgencyOS-Retrospective/reusable_assets_and_learnings.md

# AgencyOS-vs-Copilots
mv docs/research/AgencyOS-vs-Copilots/browser_vs_native_ai_apps.md docs/core/AgencyOS-vs-Copilots/browser_vs_native_ai_apps.md
mv docs/research/AgencyOS-vs-Copilots/strategic_evaluation.md docs/core/AgencyOS-vs-Copilots/strategic_evaluation.md

# kinetik-os-analysis
mv docs/research/kinetik-os-analysis/comparison_report.md docs/core/kinetik-os-analysis/comparison_report.md
mv docs/research/kinetik-os-analysis/configuration_and_clinerules_analysis.md docs/technical/kinetik-os-analysis/configuration_and_clinerules_analysis.md
mv docs/research/kinetik-os-analysis/improvements_conflict_analysis.md docs/technical/kinetik-os-analysis/improvements_conflict_analysis.md
mv docs/research/kinetik-os-analysis/justification_for_archiving_plan.md docs/operations/kinetik-os-analysis/justification_for_archiving_plan.md
mv docs/research/kinetik-os-analysis/kinetik_faults_and_remedies.md docs/technical/kinetik-os-analysis/kinetik_faults_and_remedies.md
mv docs/research/kinetik-os-analysis/public_repo_security_audit.md docs/technical/kinetik-os-analysis/public_repo_security_audit.md
mv docs/research/kinetik-os-analysis/steps_to_fix_kinetik_os.md docs/operations/kinetik-os-analysis/steps_to_fix_kinetik_os.md

# twin_so_analysis/v1
mv docs/research/twin_so_analysis/v1/agencyos_vs_twin_so_comparative_analysis.md docs/core/twin_so_analysis/v1/agencyos_vs_twin_so_comparative_analysis.md
mv docs/research/twin_so_analysis/v1/build_vs_run_sandbox_spec.md docs/technical/twin_so_analysis/v1/build_vs_run_sandbox_spec.md
mv docs/research/twin_so_analysis/v1/starter_pods_marketplace_seed.md docs/core/twin_so_analysis/v1/starter_pods_marketplace_seed.md
mv docs/research/twin_so_analysis/v1/studio_ui_user_journey.md docs/core/twin_so_analysis/v1/studio_ui_user_journey.md
mv docs/research/twin_so_analysis/v1/twin_so_analysis.md docs/core/twin_so_analysis/v1/twin_so_analysis.md
mv docs/research/twin_so_analysis/v1/twin_so_standalone_report.md docs/core/twin_so_analysis/v1/twin_so_standalone_report.md
mv docs/research/twin_so_analysis/v1/twin_so_strategic_applications.md docs/core/twin_so_analysis/v1/twin_so_strategic_applications.md

# twin_so_analysis/v2
mv docs/research/twin_so_analysis/v2/build_vs_run_sandbox_spec.md docs/technical/twin_so_analysis/v2/build_vs_run_sandbox_spec.md
mv docs/research/twin_so_analysis/v2/compliance_audit_report.md docs/operations/twin_so_analysis/v2/compliance_audit_report.md
mv docs/research/twin_so_analysis/v2/e2e_qa_test_plan.md docs/qa/twin_so_analysis/v2/e2e_qa_test_plan.md
mv docs/research/twin_so_analysis/v2/scope_document.md docs/core/twin_so_analysis/v2/scope_document.md
mv docs/research/twin_so_analysis/v2/starter_pods_marketplace_seed.md docs/core/twin_so_analysis/v2/starter_pods_marketplace_seed.md
mv docs/research/twin_so_analysis/v2/studio_ui_user_journey.md docs/core/twin_so_analysis/v2/studio_ui_user_journey.md

# Remove empty directories
rm -rf docs/research/AgencyOS-Lite
rm -rf docs/research/AgencyOS-Retrospective
rm -rf docs/research/AgencyOS-vs-Copilots
rm -rf docs/research/kinetik-os-analysis
rm -rf docs/research/twin_so_analysis/v1
rm -rf docs/research/twin_so_analysis/v2
rm -rf docs/research/twin_so_analysis
rmdir docs/research
