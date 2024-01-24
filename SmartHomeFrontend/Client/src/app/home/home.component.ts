import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServiceService } from '../service.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Socket } from 'ngx-socket-io';
import { AlarmDialogComponent } from '../alarm-dialog/alarm-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { DmsDialogComponent } from '../dms-dialog/dms-dialog.component';
import { BirDialogComponent } from '../bir-dialog/bir-dialog.component';



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private route: ActivatedRoute,public dialog: MatDialog, private router:Router, private service: ServiceService, private socket: Socket){}
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


  public tempLCD = 0;
  public humidityLCD = 0;
  public peopleCount = 0;

  public soundOn = false;
  public soundOnDS1 = false;
  public soundOnDS2 = false;
  public soundOnPIR = false;
  public soundOnGSG = false;

  public lightDL = false;

  public b4sd = "00:00"

  public colorRGB  = "white";
  public turnOffrgb = ""


  isButtonEnableCancelAlarm: boolean = false;






  ngOnInit(): void {
    this.refresh();
    this.displayCurrentTime();
    

    this.socket.fromEvent<string>('brgb')
      .subscribe((message: any) => {
        console.log(message)
        if (message.value === 'light_blue'){
          this.colorRGB = "rgb(94, 166, 233)"
          this.turnOffrgb = 'Turn on'
        }else if (message.value === 'turnOff'){
          this.colorRGB = 'white'
          this.turnOffrgb = 'Turn off'
        }else{
          this.colorRGB =message.value
          this.turnOffrgb = 'Turn on'
        }
         
      });
    
    this.socket.fromEvent<string>('glcd')
      .subscribe((message: any) => {
        if (message.measurement === 'Temperature') {
          this.tempLCD = message.value;
        } else if (message.measurement === 'Humidity') {
          this.humidityLCD = message.value;
        }
      });

      this.socket.fromEvent<string>('dl')
      .subscribe((message: any) => {
        console.log(message);
          this.lightDL = message;
      });


    this.socket.fromEvent<string>('people')
      .subscribe((message: any) => {
        this.peopleCount = message;
      });

    this.socket.fromEvent<string>('system-activated')
      .subscribe((message: any) => {
        this.soundOnDS1 = false;
        this.soundOnDS2 = false;
        this.soundOnPIR = false;
        this.soundOnGSG = false;
        this.displayCurrentTime();
      });

      this.socket.fromEvent<string>('alarm-DS')
      .subscribe((message: any) => {
        if (message.name === 'DS1'){
          this.soundOnDS1 = message.value
          
        }else{
          this.soundOnDS2 = message.value
        }
        this.displayCurrentTime();
      });

      this.socket.fromEvent<string>('alarm-PIR')
      .subscribe((message: any) => {
        if (message == true){
          this.soundOnPIR = true;
        }else{
          this.soundOnPIR = false;
        }
        this.displayCurrentTime();
      });

      this.socket.fromEvent<string>('alarm-GSG')
      .subscribe((message: any) => {
        if (message == true){
          this.soundOnGSG = true;
        }else{
          this.soundOnGSG = false;
        }
        this.displayCurrentTime();
      });

      this.socket.fromEvent<string>('alarm-oclock')
      .subscribe((message: any) => {
        if (message == true){
          this.isButtonEnableCancelAlarm = true;
          this.soundOn = true;

        }else{
          this.soundOn = false;
          this.isButtonEnableCancelAlarm = false;
        }
        
        this.displayCurrentTime();
      });

      

  }



  openDMSDialog():void{
    const dialogRef = this.dialog.open(DmsDialogComponent);

  }

  openAlarmDialog():void{
    const dialogRef = this.dialog.open(AlarmDialogComponent);
    
  }

  openBIRDialog():void{
    const dialogRef = this.dialog.open(BirDialogComponent);
    
  }


  refresh(): void{
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

    
  }

  displayCurrentTime():void{
    this.service.b4sdChangeDevice().subscribe({next:
      (response)=>{
        const now = new Date();
          const hours = this.padZero(now.getHours());
          const minutes = this.padZero(now.getMinutes());
          this.b4sd =  `${hours}:${minutes}`
      }, error: (error)=> {
        console.error(error)
      }})


  }

  private padZero(value: number): string {
    return value < 10 ? `0${value}` : `${value}`;
  }


  stopAlarm(): void{
    this.service.cancelAlarm().subscribe({next:
      (response)=>{
      }, error: (error)=> {
        console.error(error)
      }})
  }
 
}
