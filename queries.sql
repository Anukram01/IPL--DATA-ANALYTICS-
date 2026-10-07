-- 1. Venue-Wise Toss Conversion Efficiency
SELECT 
    venue,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_and_match_wins,
    ROUND(100.0 * SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_conversion_pct
FROM matches
GROUP BY venue
HAVING COUNT(*) >= 15
ORDER BY win_conversion_pct DESC;

-- 2. Dominant Victories (Win margin >= 50 runs or >= 8 wickets)
SELECT 
    winner,
    COUNT(*) AS dominant_wins
FROM matches
WHERE win_by_runs >= 50 OR win_by_wickets >= 8
GROUP BY winner
ORDER BY dominant_wins DESC;
