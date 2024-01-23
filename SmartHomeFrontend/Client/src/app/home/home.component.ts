import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServiceService } from '../service.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Socket } from 'ngx-socket-io';



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router:Router, private service: ServiceService, private socket: Socket){}
  devices: any[] = []; 

  public rdht1T = 0;
  public rdht1H = 0;
  public rdht1S = false;

  public rdht2T = 0;
  public rdht2H = 0;
  public rdht2S = false;

  public rdht3T = 0;
  public rdht3H = 0;
  public rdht3S = false;

  public rdht4T = 0;
  public rdht4H = 0;
  public rdht4S = false;

  public gdhtT = 0;
  public gdhtH = 0;
  public gdhtS = false;




  ngOnInit(): void {
    this.service.getDevices().subscribe({
      next: (response) =>{
        for (let item of response.data){
          if(item._measurement !== 'Humidity' && item._measurement !== 'Temperature'){
            this.devices.push(item)
          }
          if(item._measurement === 'Humidity'){
            if (item.name === 'RDHT1'){
              this.rdht1H = item._value;
              this.rdht1S = item.simulated;
            } else if (item.name === 'RDHT2'){
              this.rdht2H = item._value;
              this.rdht2S = item.simulated;
            }else if (item.name === 'RDHT3'){
              this.rdht3H = item._value;
              this.rdht3S = item.simulated;
            }else if (item.name === 'RDHT4'){
              this.rdht4H = item._value;
              this.rdht4S = item.simulated;
            }else if (item.name === 'GDHT'){
              this.gdhtH = item._value;
              this.gdhtS = item.simulated;
            }
          }
          if(item._measurement === 'Temperature'){
            if (item.name === 'RDHT1'){
              this.rdht1T = item._value;
            } else if (item.name === 'RDHT2'){
              this.rdht2T = item._value;
            }else if (item.name === 'RDHT3'){
              this.rdht3T = item._value;
            }else if (item.name === 'RDHT4'){
              this.rdht4T = item._value;
            }else if (item.name === 'GDHT'){
              this.gdhtT = item._value;
            }
            
          }
        }
        console.log(this.devices)
      },
      error: (error) => {
        if (error instanceof HttpErrorResponse){
          console.log(error.error[Object.keys(error.error)[0]]);
        }
      }, 
    })

    /*this.socket.fromEvent<string>('data')
      .subscribe((message: any) => {
        console.log(message)
      
      });*/
   
  }



  openDMSDialog():void{

  }

  openAlarmDialog():void{
    
  }

  openBIRDialog():void{
    
  }


}
