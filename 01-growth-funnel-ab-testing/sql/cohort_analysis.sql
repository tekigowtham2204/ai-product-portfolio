-- =============================================================================
-- AI Agent Activation & Growth Funnel — Cohort Analysis Queries
-- =============================================================================
-- All queries run against the SQLite database produced by data/generate_data.py
-- Tables:
--   users  (user_id, cohort, signup_at, channel, signup_week)
--   events (user_id, event, occurred_at, cohort)
-- =============================================================================


-- =============================================================================
-- Query 1: Funnel Drop-off by Step
-- -----------------------------------------------------------------------------
-- Shows how many users reach each funnel milestone and the step-over-step
-- conversion rate.  The "cumulative_pct" column reveals total activation loss
-- from top to bottom of funnel.
-- =============================================================================
WITH funnel_steps AS (
    SELECT
        event,
        COUNT(DISTINCT user_id) AS users_at_step,
        CASE event
            WHEN 'signed_up'         THEN 1
            WHEN 'onboarding_step_1' THEN 2
            WHEN 'onboarding_step_2' THEN 3
            WHEN 'onboarding_step_3' THEN 4
            WHEN 'first_agent_run'   THEN 5
            WHEN 'second_agent_run'  THEN 6
            WHEN 'retained_day7'     THEN 7
            WHEN 'retained_day30'    THEN 8
            ELSE 99
        END AS step_order
    FROM events
    WHERE event IN (
        'signed_up','onboarding_step_1','onboarding_step_2','onboarding_step_3',
        'first_agent_run','second_agent_run','retained_day7','retained_day30'
    )
    GROUP BY event
),
total_signups AS (
    SELECT users_at_step AS total FROM funnel_steps WHERE event = 'signed_up'
)
SELECT
    f.step_order,
    f.event                                            AS funnel_step,
    f.users_at_step,
    ROUND(100.0 * f.users_at_step / t.total, 1)       AS cumulative_pct,
    ROUND(
        100.0 * f.users_at_step
            / LAG(f.users_at_step) OVER (ORDER BY f.step_order),
        1
    )                                                  AS step_over_step_pct
FROM funnel_steps f
CROSS JOIN total_signups t
ORDER BY f.step_order;


-- =============================================================================
-- Query 2: Cohort Retention Matrix (Weekly Signup Cohorts × Retention Day)
-- -----------------------------------------------------------------------------
-- Classic retention heatmap: each row is a signup week, columns are day-7 and
-- day-30 retention rates.  Low values in early weeks can indicate onboarding
-- regressions or seasonal effects.
-- =============================================================================
WITH signup_cohorts AS (
    SELECT
        u.user_id,
        u.signup_week,
        u.signup_at
    FROM users u
),
retention_flags AS (
    SELECT
        sc.user_id,
        sc.signup_week,
        MAX(CASE WHEN e.event = 'retained_day7'  THEN 1 ELSE 0 END) AS retained_d7,
        MAX(CASE WHEN e.event = 'retained_day30' THEN 1 ELSE 0 END) AS retained_d30
    FROM signup_cohorts sc
    LEFT JOIN events e ON e.user_id = sc.user_id
    GROUP BY sc.user_id, sc.signup_week
)
SELECT
    signup_week,
    COUNT(*)                                              AS cohort_size,
    SUM(retained_d7)                                      AS retained_day7_n,
    SUM(retained_d30)                                     AS retained_day30_n,
    ROUND(100.0 * SUM(retained_d7)  / COUNT(*), 1)       AS day7_retention_pct,
    ROUND(100.0 * SUM(retained_d30) / COUNT(*), 1)       AS day30_retention_pct
FROM retention_flags
GROUP BY signup_week
ORDER BY signup_week;


-- =============================================================================
-- Query 3: Day-7 vs Day-30 Retention by Acquisition Channel
-- -----------------------------------------------------------------------------
-- Breaks retention down by the channel that brought the user in.  This surfaces
-- whether paid/organic/referral traffic differs in downstream quality — useful
-- for budget allocation decisions.
-- =============================================================================
WITH channel_retention AS (
    SELECT
        u.user_id,
        u.channel,
        MAX(CASE WHEN e.event = 'retained_day7'  THEN 1 ELSE 0 END) AS d7,
        MAX(CASE WHEN e.event = 'retained_day30' THEN 1 ELSE 0 END) AS d30,
        MAX(CASE WHEN e.event = 'first_agent_run' THEN 1 ELSE 0 END) AS activated
    FROM users u
    LEFT JOIN events e ON e.user_id = u.user_id
    GROUP BY u.user_id, u.channel
)
SELECT
    channel,
    COUNT(*)                                          AS total_users,
    ROUND(100.0 * SUM(activated) / COUNT(*), 1)      AS activation_rate_pct,
    ROUND(100.0 * SUM(d7)  / COUNT(*), 1)            AS day7_retention_pct,
    ROUND(100.0 * SUM(d30) / COUNT(*), 1)            AS day30_retention_pct,
    -- Retention quality index: day-30 / day-7 (higher = stickier channel)
    ROUND(1.0 * SUM(d30) / NULLIF(SUM(d7), 0), 2)   AS retention_quality_index
FROM channel_retention
GROUP BY channel
ORDER BY day7_retention_pct DESC;


-- =============================================================================
-- Query 4: High Drop-off Segments (Users Who Stalled Mid-Funnel)
-- -----------------------------------------------------------------------------
-- Identifies cohort × channel combinations with the worst onboarding completion
-- rates.  The "stall_step" column shows where users most commonly stop,
-- enabling targeted intervention design.
-- =============================================================================
WITH user_max_step AS (
    SELECT
        e.user_id,
        u.cohort,
        u.channel,
        MAX(
            CASE e.event
                WHEN 'signed_up'         THEN 1
                WHEN 'onboarding_step_1' THEN 2
                WHEN 'onboarding_step_2' THEN 3
                WHEN 'onboarding_step_3' THEN 4
                WHEN 'first_agent_run'   THEN 5
                WHEN 'second_agent_run'  THEN 6
                WHEN 'retained_day7'     THEN 7
                WHEN 'retained_day30'    THEN 8
                ELSE 0
            END
        ) AS max_step_reached
    FROM events e
    JOIN users u ON u.user_id = e.user_id
    GROUP BY e.user_id, u.cohort, u.channel
),
step_names AS (
    SELECT 1 AS s, 'signed_up'         AS step_name UNION ALL
    SELECT 2,      'onboarding_step_1'               UNION ALL
    SELECT 3,      'onboarding_step_2'               UNION ALL
    SELECT 4,      'onboarding_step_3'               UNION ALL
    SELECT 5,      'first_agent_run'                 UNION ALL
    SELECT 6,      'second_agent_run'                UNION ALL
    SELECT 7,      'retained_day7'                   UNION ALL
    SELECT 8,      'retained_day30'
)
SELECT
    ums.cohort,
    ums.channel,
    sn.step_name                                                     AS stall_step,
    COUNT(*)                                                         AS users_stalled,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (PARTITION BY ums.cohort, ums.channel),
        1
    )                                                                AS pct_of_segment
FROM user_max_step ums
JOIN step_names sn ON sn.s = ums.max_step_reached
-- Exclude users who fully completed the funnel
WHERE ums.max_step_reached < 8
GROUP BY ums.cohort, ums.channel, ums.max_step_reached
ORDER BY ums.cohort, users_stalled DESC;


-- =============================================================================
-- Query 5: Time-to-Activation Distribution (Signed-up → First Agent Run)
-- -----------------------------------------------------------------------------
-- Shows the median and percentile distribution of how long it takes users to
-- run their first agent after signing up.  Outliers (>24 h) rarely convert,
-- making this a candidate guardrail metric for onboarding speed experiments.
-- =============================================================================
WITH activation_times AS (
    SELECT
        s.user_id,
        u.cohort,
        (
            julianday(a.occurred_at) - julianday(s.occurred_at)
        ) * 24.0 AS hours_to_activate
    FROM events s
    JOIN events a  ON  a.user_id = s.user_id
                   AND a.event   = 'first_agent_run'
    JOIN users  u  ON  u.user_id = s.user_id
    WHERE s.event = 'signed_up'
)
SELECT
    cohort,
    COUNT(*)                                             AS activated_users,
    ROUND(MIN(hours_to_activate), 2)                    AS min_hours,
    ROUND(AVG(hours_to_activate), 2)                    AS mean_hours,
    -- SQLite has no PERCENTILE_CONT; approximate with subquery-based median
    ROUND(
        (
            SELECT AVG(hours_to_activate)
            FROM (
                SELECT hours_to_activate
                FROM activation_times t2
                WHERE t2.cohort = activation_times.cohort
                ORDER BY hours_to_activate
                LIMIT 2 - (SELECT COUNT(*) FROM activation_times t3
                            WHERE t3.cohort = activation_times.cohort) % 2
                OFFSET (SELECT (COUNT(*)-1)/2 FROM activation_times t4
                         WHERE t4.cohort = activation_times.cohort)
            )
        ), 2
    )                                                    AS median_hours,
    ROUND(MAX(hours_to_activate), 2)                    AS max_hours
FROM activation_times
GROUP BY cohort
ORDER BY mean_hours;
