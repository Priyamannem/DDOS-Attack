# DDoS Prevention System - Verification Test
# Run this to verify everything is working

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  DDoS PREVENTION SYSTEM - BACKEND VERIFICATION" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"
$passed = 0
$failed = 0

function Test-Endpoint {
    param($Name, $Url)
    Write-Host "`n[$Name]" -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri $Url -ErrorAction Stop
        Write-Host "  ✅ PASS" -ForegroundColor Green
        Write-Host "  Response: $($response | ConvertTo-Json -Compress -Depth 2)" -ForegroundColor Gray
        $script:passed++
        return $true
    }
    catch {
        Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
        $script:failed++
        return $false
    }
}

# Test 1: Health Check
Test-Endpoint "Health Check" "$baseUrl/health"

# Test 2: Root Endpoint
Test-Endpoint "Root / Welcome" "$baseUrl/"

# Test 3: Protected Resource
Test-Endpoint "Protected Resource" "$baseUrl/protected-resource"

# Test 4: Admin Rules
Test-Endpoint "Admin - Get Rules" "$baseUrl/admin/rules"

# Test 5: Admin Logs
Test-Endpoint "Admin - Recent Logs" "$baseUrl/admin/logs/recent?limit=5"

# Test 6: Admin Stats
Test-Endpoint "Admin - Traffic Stats" "$baseUrl/admin/traffic/stats"

# Test 7: Blocked IPs
Test-Endpoint "Admin - Blocked IPs" "$baseUrl/admin/blocked_ips"

# Test 8: Whitelist
Test-Endpoint "Admin - Whitelist" "$baseUrl/admin/whitelist"

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "RESULTS: $passed passed, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "=" * 70 -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host "`n🎉 All tests passed! Backend is fully operational!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "  1. View API docs: $baseUrl/docs" -ForegroundColor White
    Write-Host "  2. Run traffic simulator: python tests/traffic_simulator.py" -ForegroundColor White
    Write-Host "  3. Test rate limiting: Send 100 rapid requests" -ForegroundColor White
}
else {
    Write-Host "`n⚠️  Some tests failed. Check the errors above." -ForegroundColor Yellow
}

Write-Host ""
