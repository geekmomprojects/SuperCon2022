# SuperCon2022
Documentation for the motion-reactive wearables workshop at SuperCon2022

## Workshop Preparation

* The motion-reactive wearables workshop takes place Saturday, Nov. 5 from 1:00 – 3:00 p.m. on the Supplyframe HQ 2nd floor. We’ll be assembling and coding motion-reactive LED headbands. All materials to make the headbands will be provided, but you will need to bring your own laptop or Chromebook for the coding portion. 
* For the coding, you will need to bring your own laptop with a USB port and WiFi. If you have your own preferred CircuitPython editor, then make sure it is installed on your laptop. If not, then please install a CircuitPython editor like Mu [https://codewith.mu/](https://codewith.mu/), which is what I’ll be using. Also please have or install a terminal emulator that you know how to use. I’ll be using Tera Term [https://ttssh2.osdn.jp/index.html.en](https://ttssh2.osdn.jp/index.html.en)
* The board we’re using is a Seeeduino XIAO nRF52840 Sense [https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html), which has an accelerometer, gyroscope, microphone, and Bluetooth built in.  We’ll discuss/demonstrate using accelerometer data to determine movement and orientation, and how to incorporate that data into your own CircuitPython LED animations using Adafruit’s CircuitPython led_animation code library. If there is extra time, we’ll look at using microphone data in sound-reactive animations and using Bluetooth control to switch between animations. If there isn’t enough time to cover it all, there will be example code on GitHub for later review.
* You will not need the CircuitPython code in advance of the workshop, as we will be downloading and installing the code during the workshop from this repository
* STL files for the 3D printed diffusers are in the "design" directory if you would like to print your own in a different shape. Transluce.nt PLA or PETG will work fine. Print with the hollow base pointed upwards. I stopped the print at 3mm height and added a layer of tulle to help hold them in the headband cover, but they will likely stay without the tulle as well.
* An SVG file for the laser cut headband cover is in the design directory. I used this laser cuttable faux leather for the fabric: [https://www.jpplus.com/saddle-collection-sheet?sku=SC079-EA](https://www.jpplus.com/saddle-collection-sheet?sku=SC079-EA)

## References
### IMUs and orientation
* Combining accelerometer/gyro data from a 6-axis IMJU: [https://www.geekmomprojects.com/gyroscopes-and-accelerometers-on-a-chip/](https://www.geekmomprojects.com/gyroscopes-and-accelerometers-on-a-chip/)

