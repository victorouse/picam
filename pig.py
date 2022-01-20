import pigpio;

pi = pigpio.pi();

PIN1 = 14;
PIN2 = 15;

pi.set_mode(PIN1, pigpio.OUTPUT);
pi.set_mode(PIN2, pigpio.OUTPUT);

pi.set_servo_pulsewidth(PIN1, 0);
pi.set_servo_pulsewidth(PIN2, 0);

pi.stop();
exit();
