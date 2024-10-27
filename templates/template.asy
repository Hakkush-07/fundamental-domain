settings.outformat = "pdf";
size(14cm);
import graph;

FUNDAMENTAL_DOMAIN

draw((-MAX_WIDTH-0.5,0) -- (MAX_WIDTH+0.5,0), EndArrow(5));
draw((0,0) -- (0,MAX_HEIGHT+0.5), EndArrow(5));

label("Im",(0,MAX_HEIGHT+0.5),NE);
label("Re",(MAX_WIDTH+0.5,0),SE);

label("$1$",(1,0),S);
label("$-1$",(-1,0),S);
label("$0$",(0,0),S);
label("$i$",(0,1),SE);

