from datetime import date
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)

class ActionItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderName = db.Column(db.String(50), nullable=False)
    receiverName = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    impactToUser = db.Column(db.String(150), nullable=False)
    priorityWeight = db.Column(db.Integer, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "ActionItem({}, {}, {}, {}, {}, {}, {})".format(senderName, receiverName, category, body, impactToUser, priorityWeight, expirationDate)

#db.create_all()

action_put_args = reqparse.RequestParser()
action_put_args.add_argument("senderName", type=str, help="SenderName of the action Item is required", required=True)
action_put_args.add_argument("receiverName", type=str, help="ReceiverName of the action Item is required", required=True)
action_put_args.add_argument("category", type=str, help="Category of the action Item is required", required=True)
action_put_args.add_argument("body", type=str, help="Body of the action Item is required", required=True)
action_put_args.add_argument("impactToUser", type=str, help="ImpactToUser of the action Item is required", required=True)
action_put_args.add_argument("priorityWeight", type=int, help="Priority of the item is required",required=True)

action_update_args = reqparse.RequestParser()
action_update_args.add_argument("senderName", type=str, help="SenderName of the action Item is required")
action_update_args.add_argument("receiverName", type=str, help="ReceiverName of the action Item is required")
action_update_args.add_argument("category", type=str, help="Category of the action Item is required")
action_update_args.add_argument("body", type=str, help="Body of the action Item is required")
action_update_args.add_argument("impactToUser", type=str, help="ImpactToUser of the action Item is required")
action_update_args.add_argument("priorityWeight", type=int, help="Priority of the item is required")

resource_fields = {
    'id': fields.Integer,
    'senderName': fields.String,
    'receiverName': fields.String,
    'category': fields.String,
    'body': fields.String,
    'impactToUser': fields.String,
    'priorityWeight': fields.Integer,
    'expirationDate':  fields.DateTime
}

class ActionItem(Resource):
    @marshal_with(resource_fields)
    def get(self, actionItem_Id):
        result = ActionItemModel.query.filter_by(id=actionItem_Id).first()
        if not result:
            abort(404, message="Could not find action item with that id....")
        return result

    @marshal_with(resource_fields)
    def put(self, actionItem_Id):
        args = action_put_args.parse_args()
        result = ActionItemModel.query.filter_by(id=actionItem_Id).first()
        if result:
            abort(409, message="Action Item Id taken")
        actionItem = ActionItemModel(
            id=actionItem_Id,
            senderName=args['senderName'],
            receiverName=args['receiverName'],
            category=args['category'],
            body=args['body'],
            impactToUser=args['impactToUser'],
            priorityWeight=args['priorityWeight'])
        db.session.add(actionItem)
        db.session.commit()
        return actionItem, 201

    @marshal_with(resource_fields)
    def patch(self, actionItem_Id):
        args = action_update_args.parse_args()
        result = ActionItemModel.query.filter_by(id=actionItem_Id).first()
        if not result:
            abort(409, message="Action Item Id taken")
        
        if args['senderName']:
            result.senderName = args['senderName']
        if args['receiverName']:
            result.receiverName = args['receiverName']
        if args['category']:
            result.category = args['category']
        if args['body']:
            result.body = args['body']
        if args['impactToUser']:
            result.impactToUser = args['impactToUser']
        if args['priorityWeight']:
            result.priorityWeight = args['priorityWeight']

        db.session.commit()

        return result

    def delete(self, actionItem_Id):
        del actionItems[actionItem_Id]
        return '', 204

api.add_resource(ActionItem, "/actionItem/<int:actionItem_Id>")

if __name__ == "__main__":
    app.run(debug=True)