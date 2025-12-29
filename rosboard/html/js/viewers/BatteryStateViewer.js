"use strict";

class BatteryStateViewer extends Viewer {
  /**
    * Gets called when Viewer is first initialized.
    * @override
  **/
  onCreate() {
    this.viewerNode = $('<div></div>')
      .css({'font-size': '11pt'})
      .appendTo(this.card.content);

    this.img = $('<img></img>')
      .css({'width': '100px'})
      .appendTo(this.viewerNode);

    this.volts = $('<span></span>')
      .css({
	      "width": "100%",
	      "font-size": "14pt",
              "padding": "10px",
      })
      .appendTo(this.viewerNode);

    super.onCreate();
  }

  onData(msg) {
    this.card.title.text(msg._topic_name);
    let voltage = msg.voltage.toFixed(2);
    // These images are from wikipedia https://upload.wikimedia.org/wikipedia/commons/8/8e/A_colored_battery_indicator_symbol_[0-4].svg
    let img = 'battery0.svg';
    if (voltage > 12.4) {
      img = 'battery4.svg';
    } else if (voltage > 12.2) {
      img = 'battery3.svg';
    } else if (voltage > 12.1) {
      img = 'battery2.svg';
    } else if (voltage > 12.0) {
      img = 'battery1.svg';
    }
    this.volts.text(`Voltage: ${voltage}V`);
    this.img[0].src = `/images/${img}`;
  }  
}

BatteryStateViewer.friendlyName = "BatteryState";

BatteryStateViewer.supportedTypes = [
    "sensor_msgs/msg/BatteryState",
];

BatteryStateViewer.maxUpdateRate = 24.0;

Viewer.registerViewer(BatteryStateViewer);
