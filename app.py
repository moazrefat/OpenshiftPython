import os
import sys
from flask import Flask, jsonify, json, request, Response
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
PrometheusMetrics(app)

configjson = [
  {
    "name": "datacenter-1",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "false",
          "value": "300m"
        }
      }
    }
  },
  {
    "name": "datacenter-2",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "true",
          "value": "250m"
        }
      }
    }
  },
]

nutrition = [
  {
    "name": "burger-nutrition",
    "metadata": {
      "calories": 230,
      "fats": {
        "saturated-fat": "0g",
        "trans-fat": "1g"
      },
      "carbohydrates": {
          "dietary-fiber": "4g",
          "sugars": "1g"
      },
      "allergens": {
        "nuts": "false",
        "seafood": "false",
        "eggs": "true"
      }
    }
  },
]

@app.route('/configs', methods=['GET', 'POST'])
def configs():
    if request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            configjson.append(content)
            return jsonify(configjson), 200
            # return Response(json.dumps(content),  mimetype='application/json')
    else:
        return jsonify(configjson) , 200

@app.route('/configs/<item>', methods=['DELETE'])
def configDelete(item):
    deleted = False
    for index in range(len(configjson)):
        # for key in configjson[index]:
        #     # configjson.remove(item)
        #     print(configjson[index][key])
        #     deleted = True
        for dic in configjson:
            if dic['name'] == item:
                configjson.remove(dic)
                deleted = True
    if deleted:
        return jsonify(configjson) , 200
    else:
        return Response("", status=400, mimetype='application/json')

@app.route('/configs/burger-nutrition')
def configsNutrition():
    return jsonify(nutrition), 200


if __name__ == '__main__':
    # app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    # port = os.environ['SERVE_PORT']
    app.run(host=host, port=8080, threaded=True)
    if not port:
        sys.exit(1)
    else:
        app.run(host=host, port=port, threaded=True)