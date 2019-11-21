import {Component, Input, OnInit} from '@angular/core';
import * as $ from 'jquery';

@Component({
  selector: 'app-zoom-image',
  templateUrl: './zoom-image.component.html',
  styleUrls: ['./zoom-image.component.scss']
})
export class ZoomImageComponent implements OnInit {

  @Input() url: string;

  constructor() { }

  ngOnInit() {
    let thiss = this;

    $('.tile')
      // tile mouse actions
      .on('mouseover', function(){
        $(this).children('.photo').css({'transform': 'scale('+ $(this).attr('data-scale') +')'});
      })
      .on('mouseout', function(){
        $(this).children('.photo').css({'transform': 'scale(1)'});
      })
      .on('mousemove', function(e){
        $(this).children('.photo').css({'transform-origin': ((e.pageX - $(this).offset().left) / $(this).width()) * 100 + '% ' + ((e.pageY - $(this).offset().top) / $(this).height()) * 100 +'%'});
      })
      // tiles set up
      .each(function(){
        $(this)
          // add a photo container
          .append('<div class="photo"></div>')
          // some text just to show zoom level on current item in this example
          // set up a background image for each tile based on data-image attribute
          .children('.photo').css({'background-image': 'url('+ thiss.url+')', 'background-size': 'cover', 'height': '100%'});
      })
  }

  ngOnChanges() {
    let thiss = this;
    $('.photo').css({'background-image': 'url('+ thiss.url+')', 'background-size': 'cover', 'height': '100%'})
  }

}
