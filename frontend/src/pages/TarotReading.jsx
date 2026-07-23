import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import tarotService from '../services/tarotService';
import authService from '../services/authService';

/**
 * TarotReading Component
 * Connects to the existing FastAPI three-card tarot endpoint.
 */
const TarotReading = () => {
  const navigate = useNavigate();
  const [question, setQuestion] = useState('What does my future look like?');
  const [reading, setReading] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [historyGroups, setHistoryGroups] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState('');
  const [expandedGroupKey, setExpandedGroupKey] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState('');
  const [detailEntry, setDetailEntry] = useState(null);

  const formatDateTime = (value) => {
    if (!value) return 'Unknown';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' });
  };

  const loadHistory = async () => {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    if (!token) {
      setHistoryGroups([]);
      setHistoryError('');
      return;
    }

    setHistoryLoading(true);
    setHistoryError('');

    try {
      const data = await tarotService.getThreeCardHistory();
      const rawReadings = Array.isArray(data?.readings) ? data.readings : [];

      const groupedByQuestion = rawReadings.reduce((acc, item) => {
        const questionText = item.question?.trim() || 'Untitled Question';
        if (!acc[questionText]) {
          acc[questionText] = {
            question: questionText,
            createdAt: item.created_at,
            cards: {},
            firstReadingId: item.id,
          };
        }

        const currentTime = item.created_at ? new Date(item.created_at).getTime() : 0;
        const storedTime = acc[questionText].createdAt ? new Date(acc[questionText].createdAt).getTime() : 0;
        if (currentTime > storedTime) {
          acc[questionText].createdAt = item.created_at;
        }

        acc[questionText].cards[item.position] = item;
        return acc;
      }, {});

      const groupedArray = Object.values(groupedByQuestion)
        .map((group) => ({
          ...group,
          groupKey: `${group.question}-${group.createdAt || 'unknown'}`,
          cards: ['Past', 'Present', 'Future']
            .map((position) => group.cards[position])
            .filter(Boolean),
        }))
        .sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));

      setHistoryGroups(groupedArray);
    } catch (err) {
      console.error('Failed to load tarot history:', err);
      setHistoryError('Unable to load your reading history right now.');
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleGenerateReading = async (e) => {
    if (e) e.preventDefault();

    if (!question.trim()) {
      setError('Please enter a question for your reading.');
      return;
    }

    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    if (!token) {
      setError('Please log in to generate a tarot reading.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await tarotService.generateThreeCardReading(question.trim());

      if (!data || !Array.isArray(data.cards) || data.cards.length === 0) {
        throw new Error('No cards were returned by the server.');
      }

      setReading(data);
      await loadHistory();
    } catch (err) {
      console.error('Failed to generate three-card reading:', err);

      if (err.response?.status === 401) {
        authService.logout();
        navigate('/login');
        return;
      }

      const errorDetail = err.response?.data?.detail;
      const responseMessage = err.response?.data?.message;

      if (typeof errorDetail === 'string') {
        setError(errorDetail);
      } else if (typeof responseMessage === 'string') {
        setError(responseMessage);
      } else if (err.message) {
        setError(`Error: ${err.message}`);
      } else {
        setError('Failed to generate the three-card reading. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (group) => {
    if (expandedGroupKey === group.groupKey) {
      setExpandedGroupKey(null);
      setDetailEntry(null);
      return;
    }

    setExpandedGroupKey(group.groupKey);
    setDetailError('');
    setDetailLoading(true);

    try {
      if (group.firstReadingId) {
        const detail = await tarotService.getThreeCardReadingDetail(group.firstReadingId);
        setDetailEntry(detail);
      } else {
        setDetailEntry(null);
      }
    } catch (err) {
      console.error('Failed to load tarot reading detail:', err);
      setDetailError('Unable to load the selected reading details right now.');
    } finally {
      setDetailLoading(false);
    }
  };

  const getCardAccent = (position) => {
    switch (position?.toLowerCase()) {
      case 'past':
        return { border: '1px solid rgba(255, 107, 107, 0.35)', background: 'linear-gradient(135deg, rgba(255,107,107,0.15), rgba(255,153,102,0.08))', shadow: '0 12px 30px rgba(255,107,107,0.15)' };
      case 'present':
        return { border: '1px solid rgba(46, 213, 115, 0.35)', background: 'linear-gradient(135deg, rgba(46,213,115,0.16), rgba(82, 183, 136, 0.08))', shadow: '0 12px 30px rgba(46,213,115,0.15)' };
      case 'future':
        return { border: '1px solid rgba(120, 119, 255, 0.35)', background: 'linear-gradient(135deg, rgba(120,119,255,0.16), rgba(138, 109, 255, 0.08))', shadow: '0 12px 30px rgba(120,119,255,0.16)' };
      default:
        return { border: '1px solid rgba(255,255,255,0.12)', background: 'rgba(255,255,255,0.04)', shadow: '0 8px 20px rgba(0,0,0,0.18)' };
    }
  };

  return (
    <div className="auth-page-container" style={{ padding: '2rem' }}>
      <div className="mystic-card" style={{ maxWidth: '960px', width: '100%' }}>
        <div className="mystic-orb"></div>
        <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.5rem', animation: 'float 3s ease-in-out infinite' }}>🎴</div>
          <h1 className="history-title" style={{ fontSize: '2rem', margin: '0 0 0.5rem 0' }}>Three-Card Tarot Reading</h1>
          <p className="subtitle">Ask your question and receive guidance from the Past, Present, and Future.</p>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '1.5rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleGenerateReading} style={{ marginBottom: '1.5rem' }}>
          <label htmlFor="tarot-question" style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontWeight: '600' }}>
            Your Question
          </label>
          <input
            id="tarot-question"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="What does my future look like?"
            style={{
              width: '100%',
              padding: '0.95rem 1rem',
              borderRadius: '14px',
              border: '1px solid rgba(255,255,255,0.16)',
              background: 'rgba(255,255,255,0.05)',
              color: 'var(--text-primary)',
              marginBottom: '1rem',
              boxSizing: 'border-box',
              outline: 'none',
              boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)'
            }}
          />

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.95rem', fontSize: '1.05rem' }}
            disabled={loading}
          >
            {loading ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                <span className="mystic-spinner" style={{ width: '20px', height: '20px', borderWidth: '2px', margin: 0 }}></span>
                <span>Generating your three-card reading...</span>
              </div>
            ) : (
              'Generate Three-Card Reading ✨'
            )}
          </button>
        </form>

        {loading && (
          <div style={{ padding: '2rem 0', textAlign: 'center' }}>
            <div style={{ position: 'relative', display: 'inline-flex', marginBottom: '1rem' }}>
              <div className="mystic-spinner" style={{ width: '34px', height: '34px', borderWidth: '3px' }}></div>
              <div style={{ position: 'absolute', inset: 0, borderRadius: '50%', border: '1px solid rgba(255,255,255,0.15)' }}></div>
            </div>
            <p className="subtitle" style={{ color: 'var(--accent-gold)' }}>Shuffling the deck and drawing your spread...</p>
          </div>
        )}

        {!loading && reading && (
          <div
            style={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid var(--card-border)',
              borderRadius: '16px',
              padding: '1.5rem',
              marginTop: '1rem',
              textAlign: 'left',
              animation: 'fadeInOverlay 0.4s ease'
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '1.5rem', margin: '0 0 0.5rem 0' }}>{reading.reading_type || 'Three Card Spread'}</h2>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>{reading.question || question}</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              {reading.cards.map((card, index) => {
                const cardStyle = getCardAccent(card.position);
                return (
                  <div
                    key={`${card.position || 'card'}-${index}`}
                    style={{
                      ...cardStyle,
                      borderRadius: '18px',
                      padding: '1rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.7rem',
                      boxShadow: cardStyle.shadow,
                      transform: 'translateY(-2px)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.8rem', fontWeight: '700', color: 'var(--accent-gold)', textTransform: 'uppercase', letterSpacing: '0.6px' }}>
                        {card.position || 'Card'}
                      </span>
                      <div style={{ fontSize: '1.15rem' }}>{index === 0 ? '🕊️' : index === 1 ? '✨' : '🔮'}</div>
                    </div>
                    <div style={{ padding: '0.75rem', borderRadius: '12px', background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                      <h3 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--text-primary)' }}>{card.card_name || 'Unknown Card'}</h3>
                    </div>
                    <div style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                      <div><strong>Arcana:</strong> {card.arcana || 'N/A'}</div>
                      <div><strong>Suit:</strong> {card.suit || 'N/A'}</div>
                      <div><strong>Orientation:</strong> {card.orientation || 'N/A'}</div>
                    </div>
                    <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '0.75rem' }}>
                      <h4 style={{ margin: '0 0 0.35rem 0', color: 'var(--text-secondary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Meaning</h4>
                      <p style={{ margin: 0, color: 'var(--text-primary)', lineHeight: 1.6 }}>{card.meaning || 'No meaning provided.'}</p>
                    </div>
                  </div>
                );
              })}
            </div>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ width: '100%', padding: '0.9rem', fontSize: '1rem', marginTop: '1rem' }}
              onClick={() => handleGenerateReading()}
              disabled={loading}
            >
              Draw Again ✨
            </button>
          </div>
        )}

        <div style={{ marginTop: '1.75rem', paddingTop: '1.25rem', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
            <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Reading History</h2>
            <button
              type="button"
              className="btn btn-secondary"
              style={{ padding: '0.7rem 1rem', fontSize: '0.95rem' }}
              onClick={loadHistory}
              disabled={historyLoading}
            >
              {historyLoading ? 'Refreshing...' : 'Refresh History'}
            </button>
          </div>

          {historyLoading && (
            <div style={{ textAlign: 'center', padding: '1rem 0' }}>
              <div className="mystic-spinner" style={{ width: '24px', height: '24px', borderWidth: '2px', margin: '0 auto 0.5rem' }}></div>
              <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Loading your reading history...</p>
            </div>
          )}

          {!historyLoading && historyError && (
            <div className="alert alert-danger">{historyError}</div>
          )}

          {!historyLoading && !historyError && historyGroups.length === 0 && (
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Your saved three-card readings will appear here.</p>
          )}

          <div style={{ display: 'grid', gap: '1rem' }}>
            {historyGroups.map((group) => (
              <div
                key={group.groupKey}
                style={{
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '14px',
                  padding: '1rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', flexWrap: 'wrap' }}>
                  <div>
                    <h3 style={{ margin: '0 0 0.35rem 0', fontSize: '1rem' }}>{group.question}</h3>
                    <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{formatDateTime(group.createdAt)}</p>
                  </div>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ padding: '0.6rem 0.85rem', fontSize: '0.9rem' }}
                    onClick={() => handleViewDetails(group)}
                  >
                    {expandedGroupKey === group.groupKey ? 'Hide Details' : 'View Details'}
                  </button>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '0.75rem', marginTop: '0.75rem' }}>
                  {group.cards.map((card) => (
                    <div
                      key={`${group.groupKey}-${card.position}`}
                      style={{
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderRadius: '12px',
                        padding: '0.75rem',
                      }}
                    >
                      <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--accent-gold)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                        {card.position}
                      </div>
                      <div style={{ marginTop: '0.35rem', fontWeight: '600' }}>{card.card_name || 'Unknown Card'}</div>
                      <div style={{ marginTop: '0.2rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{card.orientation || 'N/A'}</div>
                    </div>
                  ))}
                </div>

                {expandedGroupKey === group.groupKey && (
                  <div style={{ marginTop: '0.9rem', padding: '0.9rem', borderRadius: '12px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)' }}>
                    {detailLoading ? (
                      <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Loading details...</p>
                    ) : detailError ? (
                      <p style={{ margin: 0, color: '#ff6b6b' }}>{detailError}</p>
                    ) : (
                      <>
                        {detailEntry && (
                          <div style={{ marginBottom: '0.75rem' }}>
                            <div style={{ fontSize: '0.8rem', fontWeight: '700', color: 'var(--accent-gold)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Selected Detail</div>
                            <div style={{ marginTop: '0.25rem', fontWeight: '600' }}>{detailEntry.card_name || 'Unknown Card'}</div>
                            <div style={{ marginTop: '0.2rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                              {detailEntry.position} • {detailEntry.orientation || 'N/A'}
                            </div>
                          </div>
                        )}
                        <div style={{ display: 'grid', gap: '0.5rem' }}>
                          {group.cards.map((card) => (
                            <div key={`${group.groupKey}-detail-${card.position}`}>
                              <strong>{card.position}</strong>: {card.card_name || 'Unknown'} — {card.orientation || 'N/A'}
                            </div>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TarotReading;
