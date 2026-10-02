documents = [
    {
        "id": "normal_change",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        Normal changes follow the standard change management process.
        They should be reviewed for risk, impact, implementation steps,
        validation activities, and rollback procedures before implementation.
        """
    },
    {
        "id": "emergency_change",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        Emergency changes are implemented to address critical incidents,
        outages, security issues, or other urgent situations.
        Emergency changes may follow an expedited approval process,
        but documentation and post-implementation review are still required.
        """
    },
    {
        "id": "cab",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        The Change Advisory Board reviews significant changes and considers
        business impact, technical risk, implementation plans, validation,
        rollback procedures, scheduling, and dependencies.
        """
    },
    {
        "id": "rollback",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        A rollback plan describes how to restore the previous stable state
        if a change fails. The rollback procedure should be documented,
        tested when appropriate, and available before implementation.
        """
    },
    {
        "id": "production_validation",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        Production changes should include validation activities.
        Validation may include application health checks, functional testing,
        monitoring, log verification, transaction testing, and confirmation
        that the expected business functionality is working.
        """
    },
    {
        "id": "change_closure",
        "category": "Change Management",
        "type": "Procedure",
        "text": """
        After successful implementation, a change should be reviewed for
        completion. Implementation results, validation results, incidents,
        issues, and required documentation should be recorded before closure.
        """
    },
# ]
# release_management_documents = [
    {
        "id": "release_planning",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        Release planning defines the scope, timeline, dependencies, and
        deliverables for an upcoming deployment. It aligns development schedules
        with operational readiness, identifies target environments, and establishes
        go/no-go milestones across involved teams.
        """,
    },
    {
        "id": "build_and_packaging",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        Build artifacts and software packages must be generated in a controlled,
        repeatable environment. Artifacts should be versioned, immutable, and
        stored in an artifact repository accompanied by release notes, bill of
        materials, and checksum verification.
        """,
    },
    {
        "id": "deployment_strategy",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        Deployments must follow defined roll-out strategies such as blue-green,
        canary, or phased rolling updates to minimize service interruption.
        The deployment strategy should document traffic routing mechanisms,
        monitoring signals, and automated abort thresholds.
        """,
    },
    {
        "id": "staging_and_uat",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        Releases must pass validation in a production-like staging environment
        prior to production release. Validation includes user acceptance testing (UAT),
        integration testing, regression suites, performance verification, and
        sign-off from designated business stakeholders.
        """,
    },
    {
        "id": "release_cutover",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        The cutover runbook details step-by-step technical actions, responsible
        engineers, maintenance window schedules, and communication plans.
        A formal go/no-go checkpoint must be executed prior to initiating cutover.
        """,
    },
    {
        "id": "post_release_verification",
        "category": "Release Management",
        "type": "Procedure",
        "text": """
        Following cutover, post-implementation smoke tests, telemetry reviews,
        and early-life support (hypercare) are conducted to ensure operational
        stability and verify that defect escape rates remain within acceptable limits.
        """,
    },
#]

# incident_management_documents = [
    {
        "id": "incident_identification_and_logging",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        Incidents are detected via automated alerts, monitoring thresholds,
        service desk tickets, or user reports. Every incident must be immediately
        logged with symptom descriptions, affected services, impact, and initial urgency.
        """,
    },
    {
        "id": "incident_categorization_and_prioritization",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        Incidents are assigned priority levels (P1 through P4) based on combined
        urgency and business impact. High-priority incidents dictate specific
        response times, escalation paths, and service level agreements (SLAs).
        """,
    },
    {
        "id": "major_incident_management",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        Critical disruptions (P1/P2) trigger the Major Incident workflow.
        This includes spinning up a dedicated incident bridge, assigning an
        Incident Commander, enforcing clear technical roles, and coordinating
        stakeholder communications at regular intervals.
        """,
    },
    {
        "id": "investigation_and_diagnosis",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        Responders analyze telemetry, system logs, recent deployments, and
        service dependencies to isolate the fault. Triage focuses on identifying
        the primary point of failure while preserving evidentiary logs for root cause analysis.
        """,
    },
    {
        "id": "resolution_and_recovery",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        The priority during active incidents is restoring service quickly,
        which may involve workarounds, traffic redirection, restarts, or rollbacks.
        Full service recovery must be confirmed through synthetic monitoring and health checks.
        """,
    },
    {
        "id": "incident_closure_and_postmortem",
        "category": "Incident Management",
        "type": "Procedure",
        "text": """
        Once service is restored, the incident is closed with recorded resolution notes.
        Major incidents require a blameless postmortem or post-incident review (PIR)
        to identify root causes, update runbooks, and create preventive action items.
        """,
    },
]