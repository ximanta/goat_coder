import { ProblemResponse } from './get_problem_api';

// Constants for cache key prefix and expiry time (24 hours in milliseconds)
const CACHE_KEY_PREFIX = 'code_space_problem_';
const CACHE_EXPIRY_TIME = 24 * 60 * 60 * 1000; // 24 hours

// Interface for cached problem, extending ProblemResponse with timestamp and category
interface CachedProblem extends ProblemResponse {
  timestamp: number;
  category: string;
}

/**
 * Retrieves a problem from session storage cache if it exists and is not expired.
 * Using sessionStorage ensures each browser tab maintains its own problem state.
 * @param {string} category - The category of the problem to fetch.
 * @returns {CachedProblem | null} - Returns the cached problem or null if not found/expired.
 */
export function getCachedProblem(category: string): CachedProblem | null {
  try {
    const cacheKey = `${CACHE_KEY_PREFIX}${category}`; // Construct cache key
    console.log('=== Cache Read Debug ===', { category, cacheKey });
    
    const cachedData = sessionStorage.getItem(cacheKey);
    console.log('Found cached data:', !!cachedData);
    
    if (!cachedData) return null;
    
    const problem: CachedProblem = JSON.parse(cachedData);
    const now = Date.now();
    
    console.log('Cache data parsed:', {
      title: problem.problem_title,
      timestamp: new Date(problem.timestamp).toISOString(),
      isExpired: now - problem.timestamp > CACHE_EXPIRY_TIME
    });
    
    // Check if the cached data has expired
    if (now - problem.timestamp > CACHE_EXPIRY_TIME) {
      console.log('Cache expired, removing');
      sessionStorage.removeItem(cacheKey);
      return null;
    }
    
    return problem; // Return valid cached problem
  } catch (error) {
    console.error('Error reading from cache:', error);
    return null;
  }
}

/**
 * Caches a problem in session storage with a timestamp for expiry tracking.
 * Using sessionStorage ensures each browser tab maintains its own problem state.
 * @param {string} category - The category of the problem.
 * @param {ProblemResponse} problem - The problem data to cache.
 */
export function setCachedProblem(category: string, problem: ProblemResponse): void {
  try {
    const cacheKey = `${CACHE_KEY_PREFIX}${category}`; // Construct cache key
    console.log('=== Cache Write Debug ===', { category, cacheKey, problemTitle: problem.problem_title });
    
    const cachedProblem: CachedProblem = {
      ...problem,
      timestamp: Date.now(), // Store current timestamp
      category
    };
    
    sessionStorage.setItem(cacheKey, JSON.stringify(cachedProblem));
    console.log('Problem cached successfully');
  } catch (error) {
    console.error('Error writing to cache:', error);
  }
}

/**
 * Clears the cached problem data for a specific category or all cached problems.
 * @param {string} [category] - Optional category to clear specific cache; clears all if not provided.
 */
export function clearProblemCache(category?: string): void {
  try {
    if (category) {
      sessionStorage.removeItem(`${CACHE_KEY_PREFIX}${category}`);
    } else {
      // Loop through session storage and remove all problem cache entries
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (key?.startsWith(CACHE_KEY_PREFIX)) {
          sessionStorage.removeItem(key);
        }
      }
    }
  } catch (error) {
    console.error('Error clearing cache:', error);
  }
}