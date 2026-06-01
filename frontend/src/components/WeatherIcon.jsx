import { motion } from 'framer-motion';
import { getWeatherEmoji } from '../utils/weatherCondition';
import './WeatherIcon.css';

export default function WeatherIcon({ condition }) {
  return (
    <motion.div
      className="weather-icon weather-icon--float"
      aria-hidden
      initial={{ scale: 0.85, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 200, damping: 18 }}
      key={condition}
    >
      {getWeatherEmoji(condition)}
    </motion.div>
  );
}
