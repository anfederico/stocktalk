function randomVolume(n, startDate) {
  startDate = startDate || new Date();
  var startYear = startDate.getUTCFullYear();
  var startMonth = startDate.getUTCMonth();
  var startDay = startDate.getUTCDate();
  var toReturn = new Array(n);
  var base = Math.random()*100
  for (var i = 0; i < n; i++) {
    draw = Math.random()
    toReturn[i] = {
      x: new Date(Date.UTC(startYear, startMonth, startDay + i/60)),
      y: draw > 0.9 && draw < 0.92 ? base + Math.random() * 100 : base +  Math.random() * 30
    };
  };
  return toReturn;
}

function randomSentiment(n, startDate) {
  startDate = startDate || new Date();
  var startYear = startDate.getUTCFullYear();
  var startMonth = startDate.getUTCMonth();
  var startDay = startDate.getUTCDate();
  var toReturn = new Array(n);
  for (var i = 0; i < n; i++) {
    toReturn[i] = {
      x: new Date(Date.UTC(startYear, startMonth, startDay + i/60)),
      y: Math.random() > 0.5 ? Math.random()/1.5 : -1 * Math.random()/1.5
    };
  };
  return toReturn;
}

function sum(array) {
  total = 0;
  for (var i = 0; i < array.length; i++) {
    total += array[i]
  }
  return total;
}

function avg(array) {
  if (array.length == 0){
    return 0
  }
  total = 0;
  for (var i = 0; i < array.length; i++) {
    total += array[i]
  }
  return total/array.length;
}

function ms(n, tf) {
  if (tf == 's') {
    return n*1000
  }
  if (tf == 'm') {
    return n*60*1000
  }
  if (tf == 'h') {
    return n*60*60*1000
  }
  if (tf == 'd') {
    return n*24*60*60*1000
  }
  if (tf == 'w') {
    return n*7*24*60*60*1000
  }
}

function resample(data, n, tf, method) {
  resampled = []
  for (var i = 0; i < data.length; i++) { 
    aggregated_stamps = [data[i]['x']]
    aggregated_values = [data[i]['y']]
    try {
      while (data[i+1]['x'].getTime() < aggregated_stamps[0].getTime()+ms(n, tf)) {
        aggregated_stamps.push(data[i+1]['x'])
        aggregated_values.push(data[i+1]['y'])
        i ++
        if (i > data.length) {
          break
        }
      }
    } catch(TypeError) {
      resampled.push({'x': aggregated_stamps[0], 'y': method(aggregated_values)})
      break
    }
    resampled.push({'x': aggregated_stamps[0], 'y': method(aggregated_values)})
  }
  return resampled
}