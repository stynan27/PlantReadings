<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mt-6">
        <v-row>
          <v-col cols="12">
            <v-img
              :src="require('../assets/tomato.jpg')"
              class="my-3"
              contain
              height="200"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col 
            class="mb-4"
            cols="12"
          >
            <h1 class="font-weight-bold mb-3">
              Plant-Box Readings
            </h1>


            <p class="subheading font-weight-regular">
              Dynamically updates based on incoming Websocket messages.
            </p>
          </v-col>
        </v-row>

        <v-row>
          <v-col
            cols="12"
          >
            <h2 class="headline font-weight-bold mb-5">
              Current datetime: {{ currentTime }}
            </h2>
          </v-col>
        </v-row>

        <v-row justify="start">
          <v-col
            class="mb-6"
            cols="12"
          >
            <h2 class="headline font-weight-bold mb-5">
              <div>
                <span>
                  Last msg recvd: 
                </span>
                <span v-if="plantData['time']">
                  {{ plantData['time'] }}
                </span>
              </div>
            </h2>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col
            cols="8"
          >
            <v-table>
              <thead>
                <tr>
                  <th class="text-left">
                    Temperature (&#176;F)
                  </th>
                  <th class="text-left">
                    Humidity (%)
                  </th>
                  <th class="text-left">
                    Pressure (hPa)
                  </th>
                  <th class="text-left">
                   Gas (&#8486; Ohms)
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="text-left">
                    <div v-if="plantData['temp']">
                      {{ plantData['temp'] }}
                    </div>
                  </td>
                  <td class="text-left">
                    <div v-if="plantData['humidity']">
                      {{ plantData['humidity'] }}
                    </div>
                  </td>
                  <td class="text-left">
                    <div v-if="plantData['pressure']">
                      {{ plantData['pressure'] }} 
                    </div>
                  </td>
                  <td class="text-left">
                    <div v-if="plantData['gas']">
                      {{ plantData['gas'] }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import { VTable } from 'vuetify/components'

  export default {
    name: 'PlantData',
    components: {
      VTable
    },
    methods: {
      getTime() {
				setInterval(()=>{
					//New date() a new data object, the current date and time
					//The tolocalestring () method converts the date object into a string according to the local time and returns the result.
					this.currentTime = new Date().toLocaleString();
				}, 1000)
			},
    },
    data: () => ({
      currentTime: new Date().toLocaleString(),
      plantData: {},
    }),
    created() {
      this.getTime();

      const socket = new WebSocket('ws://localhost:8765')

      socket.addEventListener('open', () => {
        console.log('WS connection open!');
        socket.send('Start sending me data.');
      });

      socket.addEventListener('close', () => {
        console.log('Websocket connection closed.');
      });

      socket.addEventListener('error', (error) => {
        console.error('Websocket connection has closed due to an error.');
        console.error('Error:', error);
      });

      // Listen for data message
      socket.addEventListener('message', (event) => {
        console.log('Recvd new data: ', JSON.parse(event.data), typeof JSON.parse(event.data));
        this.plantData = Object.assign({}, JSON.parse(event.data));
      });
    },
  }
</script>
