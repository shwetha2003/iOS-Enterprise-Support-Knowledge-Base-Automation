import React, { useState } from 'react';
import { runScript } from '../services/api';
import './ScriptRunner.css';

const ScriptRunner = ({ scriptName, scriptDescription, icon }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [deviceId, setDeviceId] = useState('');

  const handleRunScript = async () => {
    if (isRunning) return;
    
    setIsRunning(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await runScript(scriptName, deviceId || undefined);
      
      if (response.success) {
        setResult(response.result);
        
        // Log successful execution
        console.log(`${scriptName} executed successfully for device: ${response.device_id}`);
      } else {
        setError(response.error || 'Script execution failed');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsRunning(false);
    }
  };

  const getScriptDisplayName = () => {
    const names = {
      'network_validator': 'Network Validator',
      'mdm_checker': 'MDM Compliance Checker',
      'storage_cleaner': 'Storage Cleaner'
    };
    return names[scriptName] || scriptName;
  };

  const formatResult = (data) => {
    if (!data) return null;
    
    switch (scriptName) {
      case 'network_validator':
        return (
          <div className="script-result">
            <div className="health-score">
              <span className="score-label">Health Score:</span>
              <span className={`score-value ${data.health_score >= 80 ? 'good' : data.health_score >= 50 ? 'warning' : 'bad'}`}>
                {data.health_score}/100
              </span>
            </div>
            
            <div className="status-summary">
              <h4>Status: {data.summary?.status}</h4>
              <p>Checks: {data.summary?.passed_checks}/{data.summary?.total_checks} passed</p>
            </div>
            
            {data.issues && data.issues.length > 0 && (
              <div className="issues-section">
                <h4>Issues Found:</h4>
                <ul>
                  {data.issues.map((issue, idx) => (
                    <li key={idx} className={`issue-item ${issue.severity}`}>
                      <strong>{issue.category}:</strong> {issue.message}
                      <div className="solution">💡 {issue.solution}</div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {data.quick_fixes && (
              <div className="quick-fixes">
                <h4>Quick Fixes:</h4>
                <ul>
                  {data.quick_fixes.map((fix, idx) => (
                    <li key={idx}>{fix}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        );
        
      case 'mdm_checker':
        return (
          <div className="script-result">
            <div className="compliance-score">
              <span className="score-label">Compliance Score:</span>
              <span className={`score-value ${data.compliance_score >= 90 ? 'good' : 'bad'}`}>
                {data.compliance_score}/100
              </span>
              <span className="status-badge">{data.status}</span>
            </div>
            
            <div className="summary-stats">
              <div className="stat">
                <span className="stat-label">Profiles Installed:</span>
                <span className="stat-value">
                  {data.summary?.passed_checks}/{data.summary?.total_checks}
                </span>
              </div>
              <div className="stat">
                <span className="stat-label">Critical Issues:</span>
                <span className="stat-value critical">{data.summary?.critical_issues}</span>
              </div>
            </div>
            
            {data.issues && data.issues.length > 0 && (
              <div className="compliance-issues">
                <h4>Compliance Issues:</h4>
                {data.issues.map((issue, idx) => (
                  <div key={idx} className={`compliance-issue ${issue.severity}`}>
                    <div className="issue-header">
                      <span className="issue-type">{issue.type}</span>
                      <span className="issue-severity">{issue.severity}</span>
                    </div>
                    <p className="issue-message">{issue.issue || issue.message}</p>
                    <p className="issue-action">✅ {issue.action}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
        
      case 'storage_cleaner':
        return (
          <div className="script-result">
            <div className="storage-summary">
              <h4>Storage Analysis</h4>
              <div className="storage-breakdown">
                <div className="storage-total">
                  <span>Total: {data.storage_summary?.total} GB</span>
                  <span>Used: {data.storage_summary?.used} GB</span>
                  <span>Available: {data.storage_summary?.available} GB</span>
                </div>
                <div className="usage-percentage">
                  <div 
                    className="usage-bar" 
                    style={{ width: `${data.storage_summary?.percentage_used || 0}%` }}
                  ></div>
                </div>
                <span>{data.storage_summary?.percentage_used}% used</span>
              </div>
            </div>
            
            {data.potential_savings_gb > 0 && (
              <div className="savings-highlight">
                <h4>🎯 Potential Savings: {data.potential_savings_gb} GB</h4>
              </div>
            )}
            
            {data.cleanup_plan && (
              <div className="cleanup-plan">
                <h4>Cleanup Plan:</h4>
                <div className="plan-section">
                  <h5>Quick Clean ({data.cleanup_plan.quick_clean?.length || 0} tasks)</h5>
                  {data.cleanup_plan.quick_clean?.map((task, idx) => (
                    <div key={idx} className="cleanup-task">
                      <span className="task-name">{task.task}</span>
                      <span className="task-time">{task.time}</span>
                      <span className="task-savings">{task.savings}</span>
                    </div>
                  ))}
                </div>
                
                <div className="plan-section">
                  <h5>Deep Clean ({data.cleanup_plan.deep_clean?.length || 0} tasks)</h5>
                  {data.cleanup_plan.deep_clean?.map((task, idx) => (
                    <div key={idx} className="cleanup-task">
                      <span className="task-name">{task.task}</span>
                      <span className="task-time">{task.time}</span>
                      <span className="task-savings">{task.savings}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
        
      default:
        return <pre>{JSON.stringify(data, null, 2)}</pre>;
    }
  };

  return (
    <div className="script-runner-card">
      <div className="script-header">
        <div className="script-icon">{icon || '⚙️'}</div>
        <div className="script-info">
          <h3>{getScriptDisplayName()}</h3>
          <p className="script-description">{scriptDescription}</p>
        </div>
      </div>
      
      <div className="script-controls">
        <input
          type="text"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
          placeholder="Optional: Enter device identifier"
          className="device-input"
        />
        
        <button
          onClick={handleRunScript}
          disabled={isRunning}
          className={`run-button ${isRunning ? 'running' : ''}`}
        >
          {isRunning ? (
            <>
              <span className="spinner"></span>
              Running...
            </>
          ) : (
            'Run Script'
          )}
        </button>
      </div>
      
      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {result && (
        <div className="script-results">
          <div className="results-header">
            <h4>Results</h4>
            <button
              onClick={() => setResult(null)}
              className="close-results"
              aria-label="Close results"
            >
              ✕
            </button>
          </div>
          {formatResult(result)}
          
          <div className="results-actions">
            <button
              onClick={() => navigator.clipboard.writeText(JSON.stringify(result, null, 2))}
              className="action-btn"
            >
              📋 Copy Results
            </button>
            <button
              onClick={() => window.print()}
              className="action-btn"
            >
              🖨️ Print Report
            </button>
          </div>
        </div>
      )}
      
      <div className="script-tips">
        <p><strong>💡 Tip:</strong> This is a simulation. In production, this would connect to actual iOS devices via MDM APIs.</p>
      </div>
    </div>
  );
};

export default ScriptRunner;
