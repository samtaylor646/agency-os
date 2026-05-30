#!/bin/bash

# Recreate research directories
mkdir -p docs/research/AgencyOS-Lite
mkdir -p docs/research/AgencyOS-Retrospective
mkdir -p docs/research/AgencyOS-vs-Copilots
mkdir -p docs/research/kinetik-os-analysis
mkdir -p docs/research/twin_so_analysis/v1
mkdir -p docs/research/twin_so_analysis/v2

# Move general research files back
mv docs/core/Competitive_Analysis.md docs/research/Competitive_Analysis.md
mv docs/technical/dependency_audit_report.md docs/research/dependency_audit_report.md
mv docs/core/Feasibility_Studies.md docs/research/Feasibility_Studies.md
mv docs/core/Market_Trends_and_Opportunities.md docs/research/Market_Trends_and_Opportunities.md
mv docs/operations/Regulatory_and_Compliance_Research.md docs/research/Regulatory_and_Compliance_Research.md
mv docs/core/User_Insights_and_Personas.md docs/research/User_Insights_and_Personas.md

# AgencyOS-Lite back
mv docs/core/AgencyOS-Lite/Market_and_Competitor_Analysis.md docs/research/AgencyOS-Lite/Market_and_Competitor_Analysis.md
mv docs/technical/AgencyOS-Lite/Original_Repo_Usage.md docs/research/AgencyOS-Lite/Original_Repo_Usage.md
mv docs/core/AgencyOS-Lite/Product_Exploration_Lite.md docs/research/AgencyOS-Lite/Product_Exploration_Lite.md

# AgencyOS-Retrospective back
mv docs/operations/AgencyOS-Retrospective/reusable_assets_and_learnings.md docs/research/AgencyOS-Retrospective/reusable_assets_and_learnings.md

# AgencyOS-vs-Copilots back
mv docs/core/AgencyOS-vs-Copilots/browser_vs_native_ai_apps.md docs/research/AgencyOS-vs-Copilots/browser_vs_native_ai_apps.md
mv docs/core/AgencyOS-vs-Copilots/strategic_evaluation.md docs/research/AgencyOS-vs-Copilots/strategic_evaluation.md

# kinetik-os-analysis back
mv docs/core/kinetik-os-analysis/comparison_report.md docs/research/kinetik-os-analysis/comparison_report.md
mv docs/technical/kinetik-os-analysis/configuration_and_clinerules_analysis.md docs/research/kinetik-os-analysis/configuration_and_clinerules_analysis.md
mv docs/technical/kinetik-os-analysis/improvements_conflict_analysis.md docs/research/kinetik-os-analysis/improvements_conflict_analysis.md
mv docs/operations/kinetik-os-analysis/justification_for_archiving_plan.md docs/research/kinetik-os-analysis/justification_for_archiving_plan.md
mv docs/technical/kinetik-os-analysis/kinetik_faults_and_remedies.md docs/research/kinetik-os-analysis/kinetik_faults_and_remedies.md
mv docs/technical/kinetik-os-analysis/public_repo_security_audit.md docs/research/kinetik-os-analysis/public_repo_security_audit.md
mv docs/operations/kinetik-os-analysis/steps_to_fix_kinetik_os.md docs/research/kinetik-os-analysis/steps_to_fix_kinetik_os.md

# twin_so_analysis/v1 back
mv docs/core/twin_so_analysis/v1/agencyos_vs_twin_so_comparative_analysis.md docs/research/twin_so_analysis/v1/agencyos_vs_twin_so_comparative_analysis.md
mv docs/technical/twin_so_analysis/v1/build_vs_run_sandbox_spec.md docs/research/twin_so_analysis/v1/build_vs_run_sandbox_spec.md
mv docs/core/twin_so_analysis/v1/starter_pods_marketplace_seed.md docs/research/twin_so_analysis/v1/starter_pods_marketplace_seed.md
mv docs/core/twin_so_analysis/v1/studio_ui_user_journey.md docs/research/twin_so_analysis/v1/studio_ui_user_journey.md
mv docs/core/twin_so_analysis/v1/twin_so_analysis.md docs/research/twin_so_analysis/v1/twin_so_analysis.md
mv docs/core/twin_so_analysis/v1/twin_so_standalone_report.md docs/research/twin_so_analysis/v1/twin_so_standalone_report.md
mv docs/core/twin_so_analysis/v1/twin_so_strategic_applications.md docs/research/twin_so_analysis/v1/twin_so_strategic_applications.md

# twin_so_analysis/v2 back
mv docs/technical/twin_so_analysis/v2/build_vs_run_sandbox_spec.md docs/research/twin_so_analysis/v2/build_vs_run_sandbox_spec.md
mv docs/operations/twin_so_analysis/v2/compliance_audit_report.md docs/research/twin_so_analysis/v2/compliance_audit_report.md
mv docs/qa/twin_so_analysis/v2/e2e_qa_test_plan.md docs/research/twin_so_analysis/v2/e2e_qa_test_plan.md
mv docs/core/twin_so_analysis/v2/scope_document.md docs/research/twin_so_analysis/v2/scope_document.md
mv docs/core/twin_so_analysis/v2/starter_pods_marketplace_seed.md docs/research/twin_so_analysis/v2/starter_pods_marketplace_seed.md
mv docs/core/twin_so_analysis/v2/studio_ui_user_journey.md docs/research/twin_so_analysis/v2/studio_ui_user_journey.md

# Clean up empty directories if possible
rmdir docs/core/AgencyOS-Lite 2>/dev/null
rmdir docs/technical/AgencyOS-Lite 2>/dev/null
rmdir docs/operations/AgencyOS-Retrospective 2>/dev/null
rmdir docs/core/AgencyOS-vs-Copilots 2>/dev/null
rmdir docs/core/kinetik-os-analysis 2>/dev/null
rmdir docs/technical/kinetik-os-analysis 2>/dev/null
rmdir docs/operations/kinetik-os-analysis 2>/dev/null
rmdir docs/core/twin_so_analysis/v1 2>/dev/null
rmdir docs/technical/twin_so_analysis/v1 2>/dev/null
rmdir docs/core/twin_so_analysis/v2 2>/dev/null
rmdir docs/technical/twin_so_analysis/v2 2>/dev/null
rmdir docs/operations/twin_so_analysis/v2 2>/dev/null
rmdir docs/qa/twin_so_analysis/v2 2>/dev/null
rmdir docs/core/twin_so_analysis 2>/dev/null
rmdir docs/technical/twin_so_analysis 2>/dev/null
rmdir docs/operations/twin_so_analysis 2>/dev/null
rmdir docs/qa/twin_so_analysis 2>/dev/null

echo "Reversion complete!"
