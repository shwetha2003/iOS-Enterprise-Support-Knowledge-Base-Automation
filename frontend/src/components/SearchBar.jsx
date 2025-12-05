import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchKnowledgeBase, getSearchSuggestions } from '../services/api';
import './SearchBar.css';

const SearchBar = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchHistory, setSearchHistory] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Load search history from localStorage
    const savedHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    setSearchHistory(savedHistory.slice(0, 5));
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    
    try {
      const results = await searchKnowledgeBase(query);
      
      // Save to search history
      const newHistory = [
        { query, timestamp: new Date().toISOString() },
        ...searchHistory.filter(item => item.query !== query)
      ].slice(0, 5);
      
      setSearchHistory(newHistory);
      localStorage.setItem('searchHistory', JSON.stringify(newHistory));
      
      if (onSearchResults) {
        onSearchResults(results);
      }
      
      navigate(`/knowledge-base?q=${encodeURIComponent(query)}`);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = async (value) => {
    setQuery(value);
    
    if (value.length >= 2) {
      try {
        const suggestionsData = await getSearchSuggestions(value);
        setSuggestions(suggestionsData.suggestions || []);
      } catch (error) {
        console.error('Failed to fetch suggestions:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion.text);
    setSuggestions([]);
    
    if (suggestion.id) {
      navigate(`/knowledge-base/article/${suggestion.id}`);
    } else {
      handleSearch({ preventDefault: () => {} });
    }
  };

  const clearSearch = () => {
    setQuery('');
    setSuggestions([]);
    if (onSearchResults) {
      onSearchResults(null);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-wrapper">
          <input
            type="text"
            value={query}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Search for iOS issues (email, VPN, MDM, storage...)"
            className="search-input"
            aria-label="Search knowledge base"
          />
          
          {query && (
            <button
              type="button"
              onClick={clearSearch}
              className="clear-search-btn"
              aria-label="Clear search"
            >
              ✕
            </button>
          )}
          
          <button
            type="submit"
            className="search-btn"
            disabled={isSearching || !query.trim()}
          >
            {isSearching ? 'Searching...' : '🔍'}
          </button>
        </div>
        
        <div className="search-tips">
          <span>Try: </span>
          <button
            type="button"
            onClick={() => handleInputChange('email setup')}
            className="search-tag"
          >
            email setup
          </button>
          <button
            type="button"
            onClick={() => handleInputChange('VPN connection')}
            className="search-tag"
          >
            VPN connection
          </button>
          <button
            type="button"
            onClick={() => handleInputChange('storage full')}
            className="search-tag"
          >
            storage full
          </button>
        </div>
      </form>
      
      {/* Search Suggestions */}
      {suggestions.length > 0 && (
        <div className="suggestions-dropdown">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="suggestion-item"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              <div className="suggestion-text">
                {suggestion.text}
                {suggestion.category && (
                  <span className="suggestion-category">{suggestion.category}</span>
                )}
              </div>
              <span className="suggestion-arrow">→</span>
            </div>
          ))}
        </div>
      )}
      
      {/* Recent Searches */}
      {searchHistory.length > 0 && !query && (
        <div className="recent-searches">
          <div className="recent-searches-header">
            <span>Recent searches:</span>
            <button
              onClick={() => {
                localStorage.removeItem('searchHistory');
                setSearchHistory([]);
              }}
              className="clear-history-btn"
            >
              Clear all
            </button>
          </div>
          <div className="recent-search-tags">
            {searchHistory.map((item, index) => (
              <button
                key={index}
                onClick={() => handleInputChange(item.query)}
                className="recent-search-tag"
              >
                {item.query}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
