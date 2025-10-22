import { useState, useEffect } from 'react';

/**
 * Custom hook to create a typing effect
 * @param {string} text - The full text to display
 * @param {number} speed - Typing speed in milliseconds (default: 20)
 * @param {boolean} enabled - Whether typing effect is enabled (default: true)
 * @returns {Object} - Object containing displayedText and isTyping status
 */
export const useTypingEffect = (text, speed = 20, enabled = true) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    // If typing effect is disabled, show full text immediately
    if (!enabled) {
      setDisplayedText(text);
      setIsTyping(false);
      return;
    }

    // Reset when text changes
    setDisplayedText('');
    setIsTyping(true);

    if (!text) {
      setIsTyping(false);
      return;
    }

    let currentIndex = 0;
    const timer = setInterval(() => {
      if (currentIndex < text.length) {
        setDisplayedText(text.slice(0, currentIndex + 1));
        currentIndex++;
      } else {
        setIsTyping(false);
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed, enabled]);

  return { displayedText, isTyping };
};
