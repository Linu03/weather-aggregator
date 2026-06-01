import { motion } from 'framer-motion';

export default function AnimatedTemperature({ value }) {
  return (
    <motion.dd
      key={value}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: 'easeOut' }}
    >
      <motion.span
        initial={{ scale: 0.92 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 120, damping: 16 }}
      >
        {value.toFixed(1)} °C
      </motion.span>
    </motion.dd>
  );
}
